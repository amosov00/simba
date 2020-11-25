import logging
from datetime import datetime, timedelta

from celery_app.celeryconfig import app
from core.mechanics import InvoiceMechanics, BitcoinWrapper
from core.mechanics.notifier import SupportNotifier
from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import InvoiceExtended, InvoiceStatus

__all__ = ["rescue_stucked_invoices"]


@app.task(
    name="rescue_stucked_invoices",
    bind=True,
    retry_backoff=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
)
async def rescue_stucked_invoices(self, *args, **kwargs):
    counter = 0
    invoices = await InvoiceCRUD.aggregate(
        [
            {"$match": {
                "status": {"$in": (InvoiceStatus.WAITING, InvoiceStatus.PROCESSING, InvoiceStatus.PAID)},
            }},
            {
                "$lookup": {
                    "from": BTCTransactionCRUD.collection,
                    "localField": "_id",
                    "foreignField": "invoice_id",
                    "as": "btc_txs",
                }
            },
            {
                "$lookup": {
                    "from": EthereumTransactionCRUD.collection,
                    "localField": "_id",
                    "foreignField": "invoice_id",
                    "as": "eth_txs",
                }
            },
        ]
    )

    for invoice in invoices:
        invoice = InvoiceExtended(**invoice)
        if invoice.status == InvoiceStatus.WAITING:
            if len(invoice.btc_txs) == 0:
                address_info = await BitcoinWrapper().fetch_address_and_save(invoice.target_btc_address)
                if len(address_info.transactions_refs) != 0:
                    transaction = await BitcoinWrapper().fetch_transaction(
                        address_info.transactions_refs[0].transactions_hash
                    )
                    await InvoiceMechanics(invoice).proceed_new_transaction(transaction)

            elif invoice.created_at < datetime.now() - timedelta(hours=2):
                counter += 1
                await SupportNotifier(skip_timeout=True).invoice_stucked(invoice=invoice)

        elif invoice.status == InvoiceStatus.PAID and invoice.created_at < datetime.now() - timedelta(hours=2):
            await SupportNotifier(skip_timeout=True).invoice_stucked(invoice=invoice)
            counter += 1

    if counter:
        logging.info(f"Invoices stucked: {counter}")

    return
