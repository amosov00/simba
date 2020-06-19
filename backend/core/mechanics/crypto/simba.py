from hexbytes import HexBytes

from .base import CryptoValidation, CryptoCurrencyRate
from core.integrations.ethereum import ContractFunctionsWrapper, ContractEventsWrapper
from core.mechanics import InvoiceMechanics
from schemas import InvoiceInDB, InvoiceStatus
from config import SIMBA_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY


class SimbaWrapper(CryptoValidation, CryptoCurrencyRate):
    def __init__(self):
        self.api_wrapper = ContractFunctionsWrapper(
            SIMBA_CONTRACT,
            SIMBA_ADMIN_ADDRESS,
            SIMBA_ADMIN_PRIVATE_KEY
        )

    async def issue_tokens(self, customer_address: str, incoming_btc: int, comment: str) -> str:
        # TODO валидировать количество
        simba_to_issue = incoming_btc

        tx_hash = self.api_wrapper.issue_coins(
            customer_address, simba_to_issue, comment
        )

        return tx_hash.hex()

    async def validate_and_issue_tokens(
            self,
            invoice: InvoiceInDB,
            incoming_btc: int,
            comment: str
    ) -> str:
        InvoiceMechanics(invoice).validate()

        return await self.issue_tokens(invoice.target_eth_address, incoming_btc, comment)
