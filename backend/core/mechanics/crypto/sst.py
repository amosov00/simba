import asyncio

from bson import ObjectId
from sentry_sdk import capture_message, capture_exception

from config import SST_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY
from core.integrations.ethereum import FunctionsContractWrapper
from core.utils.email import MailGunEmail
from database.crud import UserCRUD, ReferralCRUD, InvoiceCRUD
from schemas import User, InvoiceInDB
from .base import CryptoValidation, CryptoCurrencyRate


class SSTWrapper(CryptoValidation, CryptoCurrencyRate):
    REF1_PROF = 0.625
    REF2_PROF = 0.125
    REF3_PROF = 0.125
    REF4_PROF = 0.0625
    REF5_PROF = 0.0625
    PERIOD: int = 2500000

    def __init__(self, invoice: InvoiceInDB):
        self.api_wrapper = FunctionsContractWrapper(SST_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY)
        self.invoice = invoice
        assert invoice is not None

    @classmethod
    def _calculate_referrals_accurals(cls, ref_level: int, sst_tokens: int) -> int:
        result_sst = sst_tokens
        if ref_level == 1:
            result_sst *= cls.REF1_PROF
        if ref_level == 2:
            result_sst *= cls.REF2_PROF
        if ref_level == 3:
            result_sst *= cls.REF3_PROF
        if ref_level == 4:
            result_sst *= cls.REF4_PROF
        if ref_level == 5:
            result_sst *= cls.REF5_PROF
        return round(result_sst)

    async def _freeze_and_transfer(self, customer_address: str, amount: int) -> str:
        try:
            tx_hash = await self.api_wrapper.freeze_and_transfer(customer_address, amount, self.PERIOD)
        except ValueError as e:
            await MailGunEmail().send_message_to_support(
                "sst_transfer",
                invoice=self.invoice,
                customer_address=customer_address,
                amount=amount
            )
            capture_exception(e)
            return ""

        return tx_hash.hex()

    async def send_sst_to_referrals(self, user: User, simba_tokens: int):
        # initial wait between simba issue and sst freeze_and_transfer
        tx_hashes = set()
        sst_tokens = self.simba_to_sst(simba_tokens)
        referral = await ReferralCRUD.find_by_user_id(user.id)

        if not referral:
            capture_message(f"Referral obj is not found for user {user.email}", level="error")
            return False

        for level in range(1, 6):
            if not referral.get(f"ref{level}"):
                continue

            current_user = await UserCRUD.find_by_id(ObjectId(referral[f"ref{level}"]))

            current_user = User(**current_user)

            if current_user.user_eth_addresses:
                customer_address = current_user.user_eth_addresses[0].address

                tx_hash: str = await self._freeze_and_transfer(
                    customer_address=customer_address,
                    amount=self._calculate_referrals_accurals(level, sst_tokens),
                )
                tx_hashes.add(tx_hash) if tx_hashes else None
                await asyncio.sleep(5.0)

        if list(tx_hashes):
            tx_hashes = list({*self.invoice.sst_tx_hashes, *tx_hashes})
            await InvoiceCRUD.update_one(
                {"_id": self.invoice.id}, {"sst_tx_hashes": tx_hashes}
            )
        return True
