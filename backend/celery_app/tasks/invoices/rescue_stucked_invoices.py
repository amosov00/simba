import logging
from datetime import datetime, timedelta

from celery_app.celeryconfig import app
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
                "created_at": {"$lte": datetime.now() - timedelta(hours=0)}
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
        if invoice.status == InvoiceStatus.PAID:
            await SupportNotifier().invoice_stucked(invoice=invoice)
            counter += 1

    if counter:
        logging.info(f"Invoices stucked: {counter}")

    return
