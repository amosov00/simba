from hexbytes import HexBytes

from .base import CryptoValidation, CryptoCurrencyRate
from core.integrations.ethereum import ContractFunctionsWrapper, ContractEventsWrapper
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

        # self._validate_invoice(excepted_status=InvoiceStatus.PROCESSING)

        tx_hash = self.api_wrapper.issue_coins(
            customer_address, simba_to_issue, comment
        )

        return tx_hash.hex()

    async def issue_tokens_and_save(
            self,
            invoice: InvoiceInDB,
            customer_address: str,
            incoming_btc: int,
            comment: str
    ):
        tx_hash = await self.issue_tokens(customer_address, incoming_btc, comment)

        # TODO получаем только хэш; По нему нельзя быстро достать инфу по транзе, отдаем обратно только хэш
        # eth_tx_set = {*invoice.eth_tx, tx_hash}

        # await InvoiceCRUD.update_one(
        #     {"_id": invoice.id}, {"eth_tx": list(eth_tx_set)}
        # )

        return tx_hash
