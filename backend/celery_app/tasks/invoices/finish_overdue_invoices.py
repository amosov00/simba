import logging
from datetime import datetime, timedelta

from pydantic import ValidationError
from sentry_sdk import capture_exception

from celery_app.celeryconfig import app
from core.mechanics import BlockCypherWebhookHandler
from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import InvoiceExtended, InvoiceStatus

__all__ = ["finish_overdue_invoices"]

INVOICE_TIMEOUT = timedelta(hours=2)


@app.task(
    name="finish_overdue_invoices", bind=True, soft_time_limit=55, time_limit=300,
)
async def finish_overdue_invoices(self, *args, **kwargs):
    """Крон для завершения счетов, которые неактивны > 2 часов и у которых нет транзакций"""
    invoices = await InvoiceCRUD.aggregate(
        [
            {"$match": {"status": {"$in": (InvoiceStatus.CREATED, InvoiceStatus.WAITING)}}},
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
    counter = 0
    for invoice in invoices:
        try:
            invoice = InvoiceExtended(**invoice)
        except ValidationError as e:
            capture_exception(e)
            continue

        if all(
                [
                    invoice.created_at + INVOICE_TIMEOUT < datetime.now(),
                    not bool(invoice.eth_txs),
                    not bool(invoice.btc_txs),
                ]
        ):
            await InvoiceCRUD.update_one({"_id": invoice.id}, {"status": InvoiceStatus.CANCELLED})
            # Delete connected webhook
            await BlockCypherWebhookHandler().delete_webhook(invoice)
            counter += 1

    if counter:
        logging.info(f"Closed {counter} overdue invoices")
    return True
