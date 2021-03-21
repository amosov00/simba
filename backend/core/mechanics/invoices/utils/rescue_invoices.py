import logging
from datetime import datetime, timedelta
from typing import Optional

from core.mechanics.crypto import BitcoinWrapper
from core.mechanics.invoices.mechanics import InvoiceMechanics
from core.mechanics.notifier import SupportNotifier
from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import InvoiceExtended, InvoiceStatus, InvoiceType, BTCTransaction

__all__ = ["rescue_stucked_invoices"]


async def _rescue_buy_invoices(invoice: InvoiceExtended) -> bool:
    if invoice.status == InvoiceStatus.WAITING:
        transaction: Optional[BTCTransaction] = None

        address_info = await BitcoinWrapper().fetch_address_and_save(invoice.target_btc_address)

        if len(address_info.transactions_refs) != 0:
            transaction = await BitcoinWrapper().fetch_transaction(address_info.transactions_refs[0].transactions_hash)

        if transaction:
            await InvoiceMechanics(invoice).proceed_new_transaction(transaction)
            return True

        elif invoice.created_at < datetime.now() - timedelta(hours=2):
            await SupportNotifier(skip_timeout=True).invoice_stucked(invoice=invoice)

    elif invoice.status == InvoiceStatus.PAID and invoice.created_at < datetime.now() - timedelta(hours=2):
        await SupportNotifier(skip_timeout=True).invoice_stucked(invoice=invoice)

    return False


async def _rescue_sell_invoices(invoice: InvoiceExtended) -> bool:
    if invoice.status == InvoiceStatus.PAID and invoice.created_at < datetime.now() - timedelta(hours=2):
        btc_tx_hash = invoice.btc_tx_hashes[0] if invoice.btc_tx_hashes else None

        if btc_tx_hash:
            transaction = await BitcoinWrapper().fetch_transaction(btc_tx_hash)
            await InvoiceMechanics(invoice).proceed_new_transaction(transaction)
            return True
        else:
            await SupportNotifier(skip_timeout=True).invoice_stucked(invoice=invoice)

    return False


async def rescue_stucked_invoices():
    invoices_rescued_counter = 0
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
        is_rescued = False

        if invoice.invoice_type == InvoiceType.BUY:
            is_rescued = await _rescue_buy_invoices(invoice)
        elif invoice.invoice_type == InvoiceType.SELL:
            is_rescued = await _rescue_sell_invoices(invoice)

        if is_rescued:
            invoices_rescued_counter += 1

    logging.info(f"Invoices stucked in queue: {len(invoices)}")
    logging.info(f"Invoices rescued: {invoices_rescued_counter}")

    return
