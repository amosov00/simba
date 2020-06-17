from typing import Literal

from database.crud import BlockCypherWebhookCRUD
from schemas import BlockCypherWebhook, BlockCypherWebhookInDB, BlockCypherWebhookEvents
from .base import BlockCypherBaseAPIWrapper


class BlockCypherWebhooksWrapper(BlockCypherBaseAPIWrapper):
    async def create_webhook(self, address: str, event: Literal[BlockCypherWebhookEvents.ALL]):  # noqa
        endpoint = "/hooks"
        data = {
            "address": address,
            "event": event
        }
        response = BlockCypherWebhook(**await self.request(endpoint, "POST", data=data, with_token=True))

        await BlockCypherWebhookCRUD.update_or_insert({"address": response.address}, response.dict())
        return response

    async def list_webhooks(self):
        endpoint = "/hooks"
        response = BlockCypherWebhook(**await self.request(endpoint, "GET", with_token=True))
        return response

    async def delete_webhook(self, webhook_id: str):
        endpoint = f"/hooks/${webhook_id}"
        response = BlockCypherWebhook(**await self.request(endpoint, "DELETE", with_token=True))
        return response

    def _validate_payload(self, token: str):
        return token == self.api_key

    async def handle(self, payload: dict):
        payload = BlockCypherWebhook(**payload)

        if not self._validate_payload(payload.token):
            return False

        if payload.event == BlockCypherWebhookEvents.UNCONFIRMED_TX:
            pass

        elif payload.event == BlockCypherWebhookEvents.TX_CONFIMATION:
            pass

        return True
