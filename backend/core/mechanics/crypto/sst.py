from hexbytes import HexBytes

from .base import CryptoValidation, CryptoCurrencyRate
from core.integrations.ethereum import ContractFunctionsWrapper, ContractEventsWrapper
from schemas import InvoiceInDB, InvoiceStatus, User
from config import SST_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY


class SSTWrapper(CryptoValidation, CryptoCurrencyRate):
    REF1_PROD = 0.625
    REF2_PROF = 0.125
    REF3_PROF = 0.125
    REF4_PROF = 0.0625
    REF5_PROF = 0.0625
    # TODO уточнить насчет периода
    PEDIOD: int = 1

    def __init__(self):
        self.api_wrapper = ContractFunctionsWrapper(
            SST_CONTRACT,
            SIMBA_ADMIN_ADDRESS,
            SIMBA_ADMIN_PRIVATE_KEY
        )

    @classmethod
    def _calculate_referrals_accurals(cls, ref_level: int, sst_tokens: int) -> float:
        # TODO дописать
        pass

    async def send_sst_to_referrals(self, user: User, simba_tokens: int):
        sst_tokens = self.simba_to_sst(simba_tokens)

        # TODO потом вызывать для каждого кошелька реферала:
        # self.api_wrapper.freeze_and_transfer(
        #     ref_address, ref_sst_tokens, self.PEDIOD,
        # )

        return True
