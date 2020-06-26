from hexbytes import HexBytes

from .base import CryptoValidation, CryptoCurrencyRate
from core.integrations.ethereum import ContractFunctionsWrapper, ContractEventsWrapper
from schemas import InvoiceInDB, InvoiceStatus, User
from config import SST_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY
from database.crud.referral import ReferralCRUD
from database.crud.user import UserCRUD


class SSTWrapper(CryptoValidation, CryptoCurrencyRate):
    REF1_PROF = 0.625
    REF2_PROF = 0.125
    REF3_PROF = 0.125
    REF4_PROF = 0.0625
    REF5_PROF = 0.0625
    # TODO уточнить насчет периода
    PERIOD: int = 1

    def __init__(self):
        self.api_wrapper = ContractFunctionsWrapper(
            SST_CONTRACT,
            SIMBA_ADMIN_ADDRESS,
            SIMBA_ADMIN_PRIVATE_KEY
        )

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
        return result_sst

    async def send_sst_to_referrals(self, user: User, simba_tokens: int):
        sst_tokens = self.simba_to_sst(simba_tokens)
        referral = await ReferralCRUD.find_by_user_id(user.id)
        for i in range(1, 6):
            user = await UserCRUD.find_by_id(referral["ref" + str(i)])
            wallet: str = user["user_eth_addresses"][0] if len(user["user_eth_addresses"]) > 0 else None
            if wallet is not None:
                self.api_wrapper.freeze_and_transfer(
                    wallet,
                    self._calculate_referrals_accurals(i, sst_tokens),
                    self.PERIOD
                )
        return True
