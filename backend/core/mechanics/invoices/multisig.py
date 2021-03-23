import asyncio
from http import HTTPStatus

from fastapi import HTTPException
from sentry_sdk import capture_message

from config import (
    IS_PRODUCTION,
    SIMBA_BUY_SELL_FEE,
    BTC_FEE,
    settings,
)
from core.mechanics.blockcypher_webhook import BlockCypherWebhookHandler
from core.mechanics.crypto import BitcoinWrapper
from database.crud import BTCTransactionCRUD
from schemas import (
    InvoiceInDB,
    BlockCypherWebhookEvents,
)
from .mechanics import InvoiceMechanics

__all__ = ["InvoiceMultisigMechanics"]


class InvoiceMultisigMechanics(InvoiceMechanics):
    async def fetch_multisig_transaction_data(self):
        """Fetch data for cosigner 1."""
        await self.validate()
        await self._validate_for_multisig()
        self._raise_exception_if_exists()

        multisig_wallet = await BitcoinWrapper().fetch_address_and_save(settings.crypto.btc_multisig_wallet_address)

        if multisig_wallet.unconfirmed_transactions_number != 0:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "wallet has outcoming transations")

        if self.invoice.simba_amount_proceeded >= multisig_wallet.balance:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "not enough balance to pay")

        spendables = await BitcoinWrapper().blockcypher_api_wrapper.get_spendables(
            settings.crypto.btc_multisig_wallet_address
        )
        payables = [(self.invoice.target_btc_address, self.invoice.simba_amount_proceeded - SIMBA_BUY_SELL_FEE)]
        return {
            "cosig1Priv": settings.crypto.btc_multisig_cosig_1_wif,
            "cosig2Pub": settings.crypto.btc_multisig_cosig_2_pub,
            "spendables": spendables,
            "payables": payables,
            "fee": BTC_FEE,
            "testnet": not IS_PRODUCTION,
        }

    async def proceed_multisig_transaction(self, transaction_hash: str) -> InvoiceInDB:
        bitcoin_wrapper = BitcoinWrapper()
        decoded_tx = await bitcoin_wrapper.blockcypher_api_wrapper.decode_tx(transaction_hash)

        # validate decoded
        self._validate_transaction(decoded_tx)
        self._raise_exception_if_exists()

        pushed_tx = await bitcoin_wrapper.blockcypher_api_wrapper.push_raw_tx(transaction_hash)

        self.invoice.btc_amount_proceeded = self.get_incoming_btc_from_outputs(
            pushed_tx.outputs, self.invoice.target_btc_address
        )
        if not self.invoice.btc_amount_proceeded:
            capture_message(f"Invalid btc amount data in TX {pushed_tx.hash}", level="error")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid btc amount data")

        self.invoice.add_hash("btc", pushed_tx.hash)
        pushed_tx.invoice_id = self.invoice.id

        await BTCTransactionCRUD.insert_one(pushed_tx.dict())
        await self.update_invoice()

        asyncio.create_task(
            BlockCypherWebhookHandler().create_webhook(
                invoice=self.invoice,
                event=BlockCypherWebhookEvents.TX_CONFIMATION,
                transaction_hash=pushed_tx.hash,
            )
        )

        return self.invoice
