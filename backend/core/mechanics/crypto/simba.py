from .base import CryptoValidation, CryptoCurrencyRate
from core.integrations.ethereum import ContractFunctionsWrapper, ContractEventsWrapper
from database.crud import InvoiceCRUD
from schemas import InvoiceInDB, InvoiceStatus
from config import SIMBA_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY


class SimbaWrapper(CryptoValidation, CryptoCurrencyRate):
    def __init__(self, invoice: InvoiceInDB):
        self.api_wrapper = ContractFunctionsWrapper(
            SIMBA_CONTRACT,
            SIMBA_ADMIN_ADDRESS,
            SIMBA_ADMIN_PRIVATE_KEY
        )
        self.invoice = invoice

    async def issue_tokens(self, customer_address: str, incoming_btc: int, comment: str):
        simba_to_issue = self.btc_to_simba_tokens(incoming_btc)

        # self._validate_invoice(excepted_status=InvoiceStatus.PROCESSING)

        tx_hash = self.api_wrapper.issue_coins(
            customer_address, simba_to_issue, comment
        )
        return await self.complete_invoice(str(tx_hash))

    async def complete_invoice(self, tx_hash: str):
        eth_tx_set = {*self.invoice.eth_tx, tx_hash}

        await InvoiceCRUD.update_one(
            {"_id": self.invoice.id},
            {
                "status": InvoiceStatus.COMPLETED,
                "eth_tx": list(eth_tx_set)
            }
        )

        return True
