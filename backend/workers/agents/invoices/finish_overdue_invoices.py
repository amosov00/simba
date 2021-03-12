import logging
from datetime import datetime, timedelta

from pydantic import ValidationError
from sentry_sdk import capture_exception

from config import INVOICE_TIMEOUT
from core.mechanics.blockcypher_webhook import BlockCypherWebhookHandler
from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import InvoiceExtended, InvoiceStatus, InvoiceType
from workers.agents import app

__all__ = ["finish_overdue_invoices_job"]

finish_overdue_invoices_topic = app.topic(
    "finish_overdue_invoices", internal=True, retention=timedelta(minutes=10), partitions=1
)


def is_btc_txs_valide(invoice) -> bool:
    if not invoice.btc_txs:
        return False

    for tx in invoice.btc_txs:
        if invoice.invoice_type == InvoiceType.SELL:
            target_btc_in_output = False

            for output in tx["outputs"]:
                if invoice.target_btc_address in output["addresses"]:
                    target_btc_in_output = True

            return target_btc_in_output

        elif invoice.invoice_type == InvoiceType.BUY:
            pass

    return bool(invoice.btc_txs)


def is_eth_txs_valide(invoice: InvoiceExtended) -> bool:
    return bool(invoice.eth_txs)


@app.agent(finish_overdue_invoices_topic, concurrency=1)
async def finish_overdue_invoices_job(stream):
    """Крон для завершения счетов, которые неактивны > 2 часов и у которых нет
    транзакций."""
    async for _ in stream:
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
                    not is_eth_txs_valide(invoice),
                    not is_btc_txs_valide(invoice),
                ]
            ):
                await InvoiceCRUD.update_one({"_id": invoice.id}, {"status": InvoiceStatus.CANCELLED})
                # Delete connected webhook
                await BlockCypherWebhookHandler().delete_webhook(invoice)
                counter += 1

        if counter:
            logging.info(f"Closed {counter} overdue invoices")

    return
