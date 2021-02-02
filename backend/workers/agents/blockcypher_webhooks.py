import logging
from datetime import timedelta

from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper
from database.crud import BlockCypherWebhookCRUD, InvoiceCRUD
from schemas import InvoiceStatus, InvoiceInDB
from workers.agents import app

__all__ = ["delete_unused_webhooks_job"]

delete_unused_webhooks_topic = app.topic(
    "delete_unused_webhooks", internal=True, retention=timedelta(minutes=30), partitions=1
)


@app.agent(delete_unused_webhooks_topic, concurrency=1)
async def delete_unused_webhooks_job(stream):
    async for _ in stream:
        counter = 0
        webhooks_blockcypher = await BlockCypherWebhookAPIWrapper().list_webhooks()
        webhooks_local = await BlockCypherWebhookCRUD.find_many({})

        for webhook in webhooks_blockcypher:
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

        for webhook in webhooks_local:
            if not list(filter(lambda o: o["id"] == webhook["id"], webhooks_blockcypher)):
                await BlockCypherWebhookCRUD.delete_one({"_id": webhook["_id"]})
                counter += 1

        if counter:
            logging.info(f"Deleted webhooks count: {counter}")
