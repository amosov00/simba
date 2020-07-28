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
    name="rescue_stucked_invoices", bind=True, soft_time_limit=55, time_limit=300,
)
async def rescue_stucked_invoices(self, *args, **kwargs):
    # TODO complete
    invoices = await InvoiceCRUD.aggregate(
        [
            {"$match": {
                "status": {"$in": (InvoiceStatus.WAITING, InvoiceStatus.PROCESSING)},
                "created_at": {"$lte": datetime.now() - timedelta(hours=3)}
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
    pass
