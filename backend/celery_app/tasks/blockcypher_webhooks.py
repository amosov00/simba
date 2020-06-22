import asyncio
from datetime import datetime, timedelta

from celery_app.celeryconfig import app
from database.crud import BlockCypherWebhookCRUD, InvoiceCRUD
from schemas import InvoiceExtended, InvoiceType, InvoiceStatus
import logging

__all__ = ['delete_unused_webhooks']


@app.task(
    name="delete_unused_webhooks",
    bind=True,
    soft_time_limit=42,
    time_limit=300,
)
async def delete_unused_webhooks(self, *args, **kwargs):
    deleted_webhooks_count = 0
    now = datetime.now()
    webhooks = await BlockCypherWebhookCRUD.find_many({
        "created_at": {"$gte": now - timedelta(hours=12)},
    })

    for webhook in webhooks:
        invoice = await InvoiceCRUD.find_one({
            "_id": webhook["invoice_id"]
        })

        if invoice:
            if invoice.status in (InvoiceStatus.COMPLETED, InvoiceStatus.CANCELLED) \
                    and invoice.created_at - now > timedelta(hours=12):
                await BlockCypherWebhookCRUD.delete_one({"_id": webhook["_id"]})
                deleted_webhooks_count += 1
            else:
                continue

        else:
            await BlockCypherWebhookCRUD.delete_one({"_id": webhook["_id"]})
            deleted_webhooks_count += 1
