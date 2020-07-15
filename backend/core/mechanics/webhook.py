from http import HTTPStatus
from urllib.parse import urljoin
from typing import Literal

from passlib import pwd
from fastapi import HTTPException
from sentry_sdk import capture_message, push_scope

from schemas import (
    InvoiceInDB,
    BlockCypherWebhookCreate,
    BlockCypherWebhookEvents,
    BlockCypherWebhookInDB,
)
from database.crud import BlockCypherWebhookCRUD
from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper
from config import HOST_URL, BTC_MINIMAL_CONFIRMATIONS

__all__ = ["BlockCypherWebhookHandler"]


class BlockCypherWebhookHandler:
    def __init__(self):
        self.api_wrapper = BlockCypherWebhookAPIWrapper()

    @staticmethod
    def _generate_webhook_url(path: str) -> str:
        return urljoin(HOST_URL, f"/api/meta/{path}/")

    @staticmethod
    async def _check_if_webhook_exists(wallet_address: str, transaction_hash: str):
        return bool(await BlockCypherWebhookCRUD.find_one(
            {"$or": [{"address": wallet_address}, {"hash": transaction_hash}]}
        ))

    async def create_webhook(
            self,
            invoice: InvoiceInDB,
            event: Literal[BlockCypherWebhookEvents.ALL],  # noqa
            wallet_address: str = None,
            transaction_hash: str = None,
    ):
        if await self._check_if_webhook_exists(wallet_address, transaction_hash):
            with push_scope() as scope:
                scope.set_level("error")
                scope.set_extra("invoice_id", str(invoice.id))
                scope.set_extra("address_or_tx_hash", wallet_address or transaction_hash)
                capture_message("webhook already exists")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "webhook already exists")

        secret_path = pwd.genword(length=10)

        webhook = BlockCypherWebhookCreate(
            url=self._generate_webhook_url(secret_path),  # noqa
            url_path=secret_path,
            invoice_id=invoice.id,
            event=event,
            token=self.api_wrapper.api_token,
            address=wallet_address,
            hash=transaction_hash,
            confirmations=BTC_MINIMAL_CONFIRMATIONS,
        )
        response = await self.api_wrapper.create_webhook(
            webhook.dict(exclude={"invoice_id", "url_path", "created_at"}, exclude_none=True)
        )
        webhook.blockcypher_id = response.get("id")
        await BlockCypherWebhookCRUD.update_or_insert({"id": webhook.blockcypher_id}, payload=webhook.dict())
        return True

    async def delete_webhook(self, invoice: InvoiceInDB) -> None:
        webhook_obj = await BlockCypherWebhookCRUD.find_one({"invoice_id": invoice.id})

        if webhook_obj:
            webhook_obj = BlockCypherWebhookInDB(**webhook_obj)
            await self.api_wrapper.delete_webhook(webhook_obj.blockcypher_id)
            await BlockCypherWebhookCRUD.delete_one({"_id": webhook_obj.id})

        return None
