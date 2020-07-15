import logging

from celery_app.celeryconfig import app
from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper
from database.crud import BlockCypherWebhookCRUD, InvoiceCRUD
from schemas import InvoiceStatus, InvoiceInDB

__all__ = ["delete_unused_webhooks"]


@app.task(
    name="delete_unused_webhooks", bind=True, soft_time_limit=42, time_limit=300,
)
async def delete_unused_webhooks(self, *args, **kwargs):
    counter = 0
    webhooks = await BlockCypherWebhookAPIWrapper().list_webhooks()

    for webhook in webhooks:
        webhook_in_db = await BlockCypherWebhookCRUD.find_one({"id": webhook.get("id")})

        if not webhook_in_db:
            continue

        invoice = await InvoiceCRUD.find_one({"_id": webhook_in_db["invoice_id"]})

        if not invoice:
            continue

        invoice = InvoiceInDB(**invoice)

        if invoice.status in (InvoiceStatus.CREATED, InvoiceStatus.COMPLETED, InvoiceStatus.CANCELLED):
            await BlockCypherWebhookAPIWrapper().delete_webhook(webhook_in_db["id"])
            await BlockCypherWebhookCRUD.delete_one({"_id": webhook_in_db["_id"]})
            counter += 1

    if counter:
        logging.info(f"Deleted webhooks count: {counter}")
    return True
