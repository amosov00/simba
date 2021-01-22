import logging
from datetime import datetime, timedelta

from core.mechanics import InvoiceMechanics, BitcoinWrapper
from core.mechanics.notifier import SupportNotifier
from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import InvoiceExtended, InvoiceStatus
from workers.agents import app

__all__ = ["rescue_stucked_invoices_job"]

rescue_stucked_invoices_topic = app.topic(
    "rescue_stucked_invoices", internal=True, retention=timedelta(minutes=10), partitions=1
)


@app.agent(rescue_stucked_invoices_topic, concurrency=1)
async def rescue_stucked_invoices_job(stream):
    async for _ in stream:
        counter = 0
        invoices = await InvoiceCRUD.aggregate(
            [
                {
                    "$match": {
                        "status": {"$in": (InvoiceStatus.WAITING, InvoiceStatus.PROCESSING, InvoiceStatus.PAID)},
                    }
                },
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

        for invoice in invoices:
            invoice = InvoiceExtended(**invoice)
            if invoice.status == InvoiceStatus.WAITING:
                if len(invoice.btc_txs) == 0:
                    address_info = await BitcoinWrapper().fetch_address_and_save(invoice.target_btc_address)
                    if len(address_info.transactions_refs) != 0:
                        transaction = await BitcoinWrapper().fetch_transaction(
                            address_info.transactions_refs[0].transactions_hash
                        )
                        await InvoiceMechanics(invoice).proceed_new_transaction(transaction)

                elif invoice.created_at < datetime.now() - timedelta(hours=2):
                    counter += 1
                    await SupportNotifier(skip_timeout=True).invoice_stucked(invoice=invoice)

            elif invoice.status == InvoiceStatus.PAID and invoice.created_at < datetime.now() - timedelta(hours=2):
                await SupportNotifier(skip_timeout=True).invoice_stucked(invoice=invoice)
                counter += 1

        if counter:
            logging.info(f"Invoices stucked: {counter}")

    return