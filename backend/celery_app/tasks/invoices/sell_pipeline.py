import asyncio, logging

from sentry_sdk import capture_message, push_scope

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
    """Крон для завершение пайплайна продажи (отсылка BTC + redeem)"""
    btc_wrapper = BitcoinWrapper()
    hot_wallet_info = await btc_wrapper.fetch_address_and_save(BTC_HOT_WALLET_ADDRESS)
    proceeding_invoices = await InvoiceCRUD.find_many({"status": InvoiceStatus.PROCESSING})

    for invoice in proceeding_invoices:
        if hot_wallet_info.unconfirmed_transactions_number:
            break

        invoice = InvoiceInDB(**invoice)
        user = await UserCRUD.find_by_id(invoice.id)

        if invoice.simba_amount_proceeded > hot_wallet_info.balance:
            with push_scope() as scope:
                scope.set_level("warning")
                scope.set_extra("Hot wallet balance", hot_wallet_info.balance)
                scope.set_extra("BTC to be sended", invoice.simba_amount_proceeded)
                scope.set_extra("Pending invoices", len(proceeding_invoices))
                capture_message("Hot wallet balance should be increased")

            break

        await InvoiceMechanics(invoice, user).send_bitcoins()

        # Wait for transaction will appear in blockchain and blockcypher
        await asyncio.sleep(15)
        # Fetch new balance and status
        hot_wallet_info = await btc_wrapper.fetch_address_and_save(BTC_HOT_WALLET_ADDRESS, save=False)

    return True
