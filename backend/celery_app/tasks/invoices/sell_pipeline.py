import asyncio, logging

from sentry_sdk import capture_message, push_scope, capture_exception

from celery_app.celeryconfig import app
from config import BTC_HOT_WALLET_ADDRESS
from core.mechanics import BitcoinWrapper, InvoiceMechanics
from core.utils import MailGunEmail
from database.crud import InvoiceCRUD, UserCRUD, MetaCRUD
from schemas import InvoiceInDB, InvoiceStatus, InvoiceType, MetaSlugs

__all__ = ["send_btc_to_proceeding_invoices"]


@app.task(
    name="send_btc_to_proceeding_invoices", bind=True, soft_time_limit=55, time_limit=300,
)
async def send_btc_to_proceeding_invoices(self, *args, **kwargs):
    """Крон для след. этапа пайплайна продажи (отсылка BTC)"""
    meta_manual_payout = await MetaCRUD.find_by_slug(MetaSlugs.MANUAL_PAYOUT)
    # Finish pipeline if manual mode
    if meta_manual_payout["payload"]["is_active"] is True:
        logging.warning("Manual mode is active")
        return True

    btc_wrapper = BitcoinWrapper()
    hot_wallet_info = await btc_wrapper.fetch_address_and_save(BTC_HOT_WALLET_ADDRESS)

    proceeding_invoices = await InvoiceCRUD.find_many({
        "invoice_type": InvoiceType.SELL,
        "status": InvoiceStatus.PROCESSING,
        "btc_tx_hashes": [],
        "btc_amount_proceeded": 0,
    }, sort=[("created_at", 1)])

    for invoice in proceeding_invoices:
        # Finish pipeline if wallet has unconfirmed transactions
        if hot_wallet_info.unconfirmed_transactions_number:
            return True

        invoice = InvoiceInDB(**invoice)
        user = await UserCRUD.find_by_id(invoice.id)
        if invoice.simba_amount_proceeded >= hot_wallet_info.balance:
            total_btc_amount_to_send = sum([
                i["simba_amount_proceeded"] for i in proceeding_invoices if i.get("simba_amount_proceeded")
            ])
            await MailGunEmail().send_message_to_support(
                "btc",
                hot_wallet_balance=hot_wallet_info.balance,
                btc_amount_to_send=invoice.simba_amount_proceeded,
                total_btc_amount_to_send=total_btc_amount_to_send,
                invoices_in_queue=len(proceeding_invoices)
            )
            with push_scope() as scope:
                scope.set_level("warning")
                scope.set_extra("Hot wallet balance", hot_wallet_info.balance)
                scope.set_extra("BTC to be sended", invoice.simba_amount_proceeded)
                scope.set_extra("Pending invoices", len(proceeding_invoices))
                capture_message("Hot wallet balance should be increased")
            break

        try:
            await InvoiceMechanics(invoice, user).send_bitcoins()
        except Exception as e:
            capture_exception(e)
            continue

        # Wait for transaction will appear in blockchain and blockcypher
        await asyncio.sleep(10)
        # Fetch new balance and status
        hot_wallet_info = await btc_wrapper.fetch_address_and_save(BTC_HOT_WALLET_ADDRESS, save=False)

    return True
