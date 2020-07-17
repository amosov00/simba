from core.integrations.ethereum import FunctionsContractWrapper
from .base import CryptoValidation, CryptoCurrencyRate
from schemas import InvoiceInDB
from config import SIMBA_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY


class SimbaWrapper(CryptoValidation, CryptoCurrencyRate):
    def __init__(self, invoice: InvoiceInDB):
        self.api_wrapper = FunctionsContractWrapper(
            SIMBA_CONTRACT, SIMBA_ADMIN_ADDRESS, SIMBA_ADMIN_PRIVATE_KEY
        )
        self.invoice = invoice

    async def issue_tokens(self, customer_address: str, incoming_btc: int, btc_tx_hash: str) -> str:
        simba_to_issue = incoming_btc

        tx_hash = await self.api_wrapper.issue_coins(customer_address, simba_to_issue, btc_tx_hash)

        return tx_hash.hex()

    async def redeem_tokens(self, outcoming_btc: int, btc_tx_hash: str):
        simba_to_redeem = outcoming_btc

        tx_hash = await self.api_wrapper.redeem_coins(simba_to_redeem, btc_tx_hash)

        return tx_hash.hex()
