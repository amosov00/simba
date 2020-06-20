import asyncio
from datetime import datetime, timedelta

from celery_app.celeryconfig import app
from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import InvoiceExtended, InvoiceType, InvoiceStatus
import logging

__all__ = ['finish_invoices_cron']


@app.task(
    name="finish_overdue_invoices",
    bind=True,
    soft_time_limit=42,
    time_limit=300,
)
async def finish_invoices_cron(self, *args, **kwargs):
    """Крон для завершения счетов, которые неактивны > 2 часов"""
    invoices = await InvoiceCRUD.aggregate([
        {"$match": {
            "status": InvoiceStatus.WAITING
        }},
        {"$lookup": {
            "from": BTCTransactionCRUD.collection,
            "localField": "_id",
            "foreignField": "invoice_id",
            "as": "btc_txs",
        }},
        {"$lookup": {
            "from": EthereumTransactionCRUD.collection,
            "localField": "_id",
            "foreignField": "invoice_id",
            "as": "eth_txs",
        }},
    ])
    tasks = []

    for invoice in invoices:
        invoice = InvoiceExtended(**invoice)
        if not all([
            datetime.now() - invoice.created_at < timedelta(hours=2),
            bool(invoice.eth_txs),
            bool(invoice.btc_txs),
        ]):
            tasks.append(InvoiceCRUD.update_one(
                {"_id": invoice.id},
                {"status": InvoiceStatus.CANCELLED}
            ))

    if tasks:
        await asyncio.gather(*tasks)
        logging.info(f"Closed {len(tasks)} invoices")

    return True
