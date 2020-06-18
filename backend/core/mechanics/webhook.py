from urllib.parse import urljoin
from uuid import uuid4
from typing import Literal

from schemas import (
    InvoiceInDB,
    BlockCypherWebhook,
    BlockCypherWebhookInDB,
    BlockCypherWebhookEvents,
    BlockCypherWebhookCreate,
)
from database.crud import BlockCypherWebhookCRUD
from config import HOST_URL, WEBHOOK_PATH
from core.integrations.blockcypher import BlockCypherWebhooksWrapper
from schemas import BlockCypherWebhook, BlockCypherWebhookInDB, BlockCypherWebhookEvents

__all__ = ["BlockCypherWebhookHandler"]


class BlockCypherWebhookHandler:
    def __init__(self):
        self.api_wrapper = BlockCypherWebhooksWrapper()

    def _validate_payload(self, token: str):
        return token == self.api_wrapper.api_key

    @staticmethod
    def _generate_webhook_id():
        return str(uuid4())

    @staticmethod
    def _generate_webhook_url() -> str:
        return urljoin(HOST_URL, f"/api/meta/{WEBHOOK_PATH}/")

    async def create_webhook(
            self,
            invoice: InvoiceInDB,
            event: Literal[BlockCypherWebhookEvents.ALL],  # noqa
            wallet_address: str = None,
            transaction_hash: str = None,
    ):
        data = BlockCypherWebhookCreate(
            id=self._generate_webhook_id(),
            url=self._generate_webhook_url(),  # noqa
            invoice_id=invoice.id,
            event=event,
            token=self.api_wrapper.api_token,
            address=wallet_address,
            hash=transaction_hash,
        )
        response = await self.api_wrapper.create_webhook(
            data.dict(exclude={"invoice_id"}, exclude_none=True)
        )
        await BlockCypherWebhookCRUD.update_or_insert({"id": data.id}, payload=data.dict())

        return True

    async def parse(self, payload: dict):
        payload = BlockCypherWebhook(**payload)

        if not self._validate_payload(payload.token):
            return False

        if payload.event == BlockCypherWebhookEvents.UNCONFIRMED_TX:
            # TODO save to DB
            pass

        elif payload.event == BlockCypherWebhookEvents.TX_CONFIMATION:
            # TODO save to DB
            pass

        return True
