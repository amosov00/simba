import asyncio

from sentry_sdk import capture_exception

from celery_app.celeryconfig import app
from config import settings
from core.mechanics import BitcoinWrapper, InvoiceMechanics
from core.mechanics.notifier import SupportNotifier
from database.crud import InvoiceCRUD, UserCRUD, MetaCRUD
from schemas import InvoiceInDB, InvoiceStatus, InvoiceType, MetaSlugs

__all__ = ["send_btc_to_proceeding_invoices"]


@app.task(
    name="send_btc_to_proceeding_invoices",
    bind=True,
    retry_backoff=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
)
async def send_btc_to_proceeding_invoices(self, *args, **kwargs):
    """Крон для след.

    этапа пайплайна продажи (отсылка BTC)
    """
    meta_manual_payout = await MetaCRUD.find_by_slug(MetaSlugs.MANUAL_PAYOUT)
    # Finish pipeline if manual mode
    if meta_manual_payout["payload"]["is_active"] is True:
        return True

    btc_wrapper = BitcoinWrapper()
    hot_wallet_info = await btc_wrapper.fetch_address_and_save(settings.crypto.btc_hot_wallet_address)

    proceeding_invoices = await InvoiceCRUD.find_many(
        {
            "invoice_type": InvoiceType.SELL,
            "status": InvoiceStatus.PROCESSING,
            "btc_tx_hashes": [],
            "btc_amount_proceeded": 0,
        },
        sort=[("created_at", 1)],
    )

    for invoice in proceeding_invoices:
        # Finish pipeline if wallet has unconfirmed transactions
        if hot_wallet_info.unconfirmed_transactions_number:
            return True

        invoice = InvoiceInDB(**invoice)
        user = await UserCRUD.find_by_id(invoice.id)

        if invoice.simba_amount_proceeded >= hot_wallet_info.balance:
            # Send alarms
            total_btc_amount_to_send = sum(
                i["simba_amount_proceeded"] for i in proceeding_invoices if i.get("simba_amount_proceeded")
            )
            await SupportNotifier().hot_wallet_balance_lack(
                hot_wallet_balance=hot_wallet_info.balance,
                btc_amount_to_send=invoice.simba_amount_proceeded,
                total_btc_amount_to_send=total_btc_amount_to_send,
                invoices_in_queue=len(proceeding_invoices),
            )
            break

        try:
            await InvoiceMechanics(invoice, user).send_bitcoins()
        except Exception as e:
            capture_exception(e)
            continue

        # Wait for transaction will appear in blockchain and blockcypher
        await asyncio.sleep(10)
        # Fetch new balance and status
        hot_wallet_info = await btc_wrapper.fetch_address_and_save(settings.crypto.btc_hot_wallet_address, save=False)

    return True
