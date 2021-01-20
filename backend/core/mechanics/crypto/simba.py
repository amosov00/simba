from sentry_sdk import capture_exception

from config import SIMBA_CONTRACT, settings
from core.integrations.ethereum import FunctionsContractWrapper
from core.utils.email import Email
from schemas import InvoiceInDB
from .base import CryptoValidation, CryptoCurrencyRate


class SimbaWrapper(CryptoValidation, CryptoCurrencyRate):
    def __init__(self):
        self.api_wrapper = FunctionsContractWrapper(
            SIMBA_CONTRACT, settings.crypto.simba_admin_address, settings.crypto.simba_admin_private_key
        )

    async def issue_tokens(
        self, customer_address: str, incoming_btc: int, btc_tx_hash: str, *, invoice: InvoiceInDB = None
    ) -> str:
        simba_to_issue = incoming_btc

        try:
            tx_hash = await self.api_wrapper.issue_coins(customer_address, simba_to_issue, btc_tx_hash)
        except ValueError as e:
            await Email().send_message_to_support(
                "simba_issue", invoice=invoice, customer_address=customer_address, amount=simba_to_issue
            )
            capture_exception(e)
            raise e

        return tx_hash.hex()

    async def redeem_tokens(self, outcoming_btc: int, btc_tx_hash: str, *, invoice: InvoiceInDB = None):
        simba_to_redeem = outcoming_btc

        try:
            tx_hash = await self.api_wrapper.redeem_coins(simba_to_redeem, btc_tx_hash)
        except ValueError as e:
            await Email().send_message_to_support("simba_redeem", invoice=invoice, amount=simba_to_redeem)
            capture_exception(e)
            raise e

        return tx_hash.hex()

    async def balance_of(self, address: str):
        return await self.api_wrapper.balance_of(address)
