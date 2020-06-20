from urllib.parse import urljoin
from typing import Literal, Optional
from datetime import datetime
import logging

from passlib import pwd
from sentry_sdk import capture_message

from schemas import (
    InvoiceInDB,
    BlockCypherWebhookCreate,
    BTCTransaction,
    BTCTransactionInDB,
    BlockCypherWebhookEvents,
    InvoiceStatus,
)
from database.crud import BlockCypherWebhookCRUD, InvoiceCRUD, BTCTransactionCRUD
from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper
from core.mechanics.crypto import SimbaWrapper
from config import HOST_URL

__all__ = ["BlockCypherWebhookHandler"]


class BlockCypherWebhookHandler:
    def __init__(self):
        self.api_wrapper = BlockCypherWebhookAPIWrapper()

    @staticmethod
    def _generate_webhook_url(path: str) -> str:
        return urljoin(HOST_URL, f"/api/meta/{path}/")

    async def create_webhook(
            self,
            invoice: InvoiceInDB,
            event: Literal[BlockCypherWebhookEvents.ALL],  # noqa
            wallet_address: str = None,
            transaction_hash: str = None,
    ):
        secret_path = pwd.genword(length=10)

        data = BlockCypherWebhookCreate(
            url=self._generate_webhook_url(secret_path),  # noqa
            url_path=secret_path,
            invoice_id=invoice.id,
            event=event,
            token=self.api_wrapper.api_token,
            address=wallet_address,
            hash=transaction_hash,
            confirmations=3,
        )
        response = await self.api_wrapper.create_webhook(
            data.dict(exclude={"invoice_id", "url_path"}, exclude_none=True)
        )
        data.blockcypher_id = response.get("id")
        await BlockCypherWebhookCRUD.update_or_insert({"id": data.blockcypher_id}, payload=data.dict())
        return True

    def validate_transaction(self) -> dict:
        pass

    async def parse(self, payload: dict):
        transaction = BTCTransaction(**payload)
        invoice = None
        incoming_btc: int = 0

        for output in transaction.outputs:
            invoice = await InvoiceCRUD.find_one({
                "target_btc_address": output.addresses[0],
                "status": {"$in": [InvoiceStatus.WAITING, InvoiceStatus.COMPLETED]}
            })
            if invoice:
                incoming_btc = output.value
                break

        if not invoice:
            capture_message(f"Invoice not founded; tx hash: {transaction.hash}")
            return True
        else:
            invoice = InvoiceInDB(**invoice)

        transaction.invoice_id = invoice.id

        if transaction_in_db := await BTCTransactionCRUD.find_one({
            "hash": transaction.hash,
        }):
            transaction_in_db = BTCTransactionInDB(**transaction_in_db)

        if transaction.block_height < 0 or transaction.confirmations == 0:
            logging.info(0)
            return True

        if transaction.confirmations < 3:
            logging.info("1")
            await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())

        # TODO transaction_in_db may not exists
        elif transaction.confirmations >= 3 and transaction_in_db.simba_tokens_issued:
            logging.info("2")
            await BTCTransactionCRUD.update_one({"hash": transaction.hash}, transaction.dict())

        elif transaction.confirmations >= 3 and not transaction_in_db.simba_tokens_issued:
            logging.info("3")
            await SimbaWrapper().validate_and_issue_tokens(
                invoice, incoming_btc=incoming_btc, comment=transaction.hash
            )
            transaction.simba_tokens_issued = True
            await BTCTransactionCRUD.update_one({"hash": transaction.hash}, transaction.dict())
            invoice.status = InvoiceStatus.COMPLETED
            invoice.btc_tx_ids = list({*invoice.btc_tx_ids, transaction_in_db.id})
            invoice.btc_amount_proceeded += incoming_btc
            invoice.finised_at = datetime.now()
            await InvoiceCRUD.update_one({"_id": invoice.id}, invoice.dict(exclude={"_id"}))

        return True
