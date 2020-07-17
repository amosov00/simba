import asyncio

from bson import ObjectId
from sentry_sdk import capture_message

from config import SST_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY
from core.integrations.ethereum import FunctionsContractWrapper
from database.crud.referral import ReferralCRUD
from database.crud.user import UserCRUD
from schemas import User
from .base import CryptoValidation, CryptoCurrencyRate


class SSTWrapper(CryptoValidation, CryptoCurrencyRate):
    REF1_PROF = 0.625
    REF2_PROF = 0.125
    REF3_PROF = 0.125
    REF4_PROF = 0.0625
    REF5_PROF = 0.0625
    PERIOD: int = 2500000

    def __init__(self):
        self.api_wrapper = FunctionsContractWrapper(SST_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY)

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

    async def send_sst_to_referrals(self, user: User, simba_tokens: int):
        # initial wait between simba issue and sst freeze_and_transfer
        await asyncio.sleep(15.0)
        sst_tokens = self.simba_to_sst(simba_tokens)
        referral = await ReferralCRUD.find_by_user_id(user.id)

        if not referral:
            capture_message(f"Referral obj is not found for user {user.email}", level="error")
            return False

        for i in range(1, 6):
            if not referral.get(f"ref{i}"):
                continue
            current_user = await UserCRUD.find_by_id(ObjectId(referral[f"ref{i}"]))
            wallet: str = current_user["user_eth_addresses"][0] if current_user.get(
                "user_eth_addresses"
            ) else None
            if wallet is not None:
                await self.api_wrapper.freeze_and_transfer(
                    wallet, self._calculate_referrals_accurals(i, sst_tokens), self.PERIOD,
                )
                # Wait between eth transations
                await asyncio.sleep(15.0)
        return True
