import asyncio, logging
from datetime import datetime, timedelta

from celery_app.celeryconfig import app
from database.crud import InvoiceCRUD, UserCRUD, EthereumTransactionCRUD
from schemas import InvoiceInDB, InvoiceStatus
from core.mechanics import BitcoinWrapper, SimbaWrapper, InvoiceMechanics
from config import BTC_HOT_WALLET_ADDRESS

__all__ = ["send_btc_to_proceeding_invoices"]


@app.task(
    name="send_btc_to_proceeding_invoices", bind=True, soft_time_limit=42, time_limit=300,
)
async def send_btc_to_proceeding_invoices(self, *args, **kwargs):
    btc_wrapper = BitcoinWrapper()
    hot_wallet_info = await btc_wrapper.fetch_address_and_save(BTC_HOT_WALLET_ADDRESS)
    proceeding_invoices = await InvoiceCRUD.find_many({"status": InvoiceStatus.PROCESSING})

    for invoice in proceeding_invoices:
        if hot_wallet_info.unconfirmed_transactions_number:
            break

        invoice = InvoiceInDB(**invoice)
        user = await UserCRUD.find_by_id(invoice.id)

        if invoice.simba_amount_proceeded > hot_wallet_info.balance:
            logging.info(f"Not enough btc on hot wallet to pay Invoice {invoice.id}")
            break

        await InvoiceMechanics(invoice, user).send_bitcoins()

        # Wait for transaction will appear in blockchain and blockcypher
        await asyncio.sleep(15)
        # Fetch new balance and status
        hot_wallet_info = await btc_wrapper.fetch_address_and_save(BTC_HOT_WALLET_ADDRESS, save=False)

    return True
