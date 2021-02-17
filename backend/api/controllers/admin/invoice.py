from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Path, Query, Response, HTTPException, Body
from sentry_sdk import capture_exception

from config import settings
from core.integrations import SimbaNodeJSWrapper
from core.mechanics import BitcoinWrapper, InvoiceMechanics, BlockCypherWebhookHandler, ReferralMechanics
from core.utils import to_objectid
from database.crud import UserCRUD, InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD, MetaCRUD
from schemas import InvoiceInDB, InvoiceExtended, InvoiceStatus, InvoiceType, MetaSlugs, ReferralTransactionUserID

__all__ = ["invoices_router"]

invoices_router = APIRouter()


@invoices_router.get(
    "/",
    response_model=List[InvoiceInDB],
)
async def admin_invoices_fetch_all(
    q: Optional[str] = Query(default=None, description="query for many fields"),
    invoice_type: Optional[str] = Query(default=None, alias="type", description="invoice type"),
    invoice_status: Optional[str] = Query(default=None, alias="status", description="invoice status"),
):
    return await InvoiceCRUD.find_by_query(q, invoice_type, invoice_status)


@invoices_router.get("/{invoice_id}/", response_model=InvoiceExtended)
async def admin_invoice_fetch_one(invoice_id: str = Path(...)):
    resp = await InvoiceCRUD.aggregate(
        [
            {"$match": {"_id": to_objectid(invoice_id)}},
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
    return resp[0] if resp else Response(status_code=404)


@invoices_router.get("/{invoice_id}/sst_transactions/", response_model=List[ReferralTransactionUserID])
async def admin_invoice_fetch_sst_tx_info(invoice_id: str = Path(...)):
    invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(invoice_id, raise_404=True))
    return await ReferralMechanics.fetch_ref_txs_info_from_invoice(invoice)


@invoices_router.post(
    "/{invoice_id}/pay/",
    response_model=InvoiceInDB,
)
async def admin_invoice_pay(invoice_id: str = Path(...)):
    invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(invoice_id, raise_404=True))

    meta_manual_payout = await MetaCRUD.find_by_slug(MetaSlugs.MANUAL_PAYOUT)
    if meta_manual_payout["payload"]["is_active"] is False:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "payout mode is auto")

    if invoice.invoice_type != InvoiceType.SELL or invoice.status != InvoiceStatus.PROCESSING:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid invoice to pay")

    hot_wallet_info = await BitcoinWrapper().fetch_address_and_save(settings.crypto.btc_hot_wallet_address)

    if hot_wallet_info.unconfirmed_transactions_number != 0:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "wallet has outcoming transations")

    if invoice.simba_amount_proceeded >= hot_wallet_info.balance:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "not enough balance to pay")

    user = await UserCRUD.find_by_id(invoice.id)
    try:
        await InvoiceMechanics(invoice, user).send_bitcoins()
    except Exception as e:
        capture_exception(e)
        raise HTTPException(HTTPStatus.BAD_REQUEST, "failed to send bitcoins")

    return await InvoiceCRUD.find_by_id(invoice.id)


@invoices_router.get(
    "/{invoice_id}/multisig/",
)
async def admin_invoice_multisig_fetch(invoice_id: str = Path(...)):
    invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(invoice_id, raise_404=True))
    data = await InvoiceMechanics(invoice).fetch_multisig_transaction_data()
    return await SimbaNodeJSWrapper().fetch_multisig_transaction(data)


@invoices_router.post(
    "/{invoice_id}/multisig/",
)
async def admin_invoice_multisig_pay(invoice_id: str = Path(...), transaction_hash: dict = Body(...)):
    transaction_hash = transaction_hash.get("transaction_hash")
    invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(invoice_id, raise_404=True))
    return await InvoiceMechanics(invoice).proceed_multisig_transaction(transaction_hash) if transaction_hash else None


@invoices_router.post("/{invoice_id}/cancel/", response_model=InvoiceInDB)
async def admin_invoice_cancel(invoice_id: str = Path(...)):
    invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(invoice_id, raise_404=True))

    if invoice.status not in (InvoiceStatus.CREATED, InvoiceStatus.WAITING, InvoiceStatus.PROCESSING):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid invoice status")

    invoice.status = InvoiceStatus.CANCELLED
    await InvoiceCRUD.update_one({"_id": invoice.id}, invoice.dict(include={"status"}))
    await BlockCypherWebhookHandler().delete_webhook(invoice)

    return invoice
