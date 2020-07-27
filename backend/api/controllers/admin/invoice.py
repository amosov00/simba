from typing import List, Literal, Optional
from http import HTTPStatus

from fastapi import APIRouter, Path, Query, Response, HTTPException
from sentry_sdk import capture_exception

from database.crud import UserCRUD, InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD, MetaCRUD
from schemas import InvoiceInDB, InvoiceExtended, InvoiceStatus, InvoiceType, MetaSlugs
from core.mechanics import BitcoinWrapper, InvoiceMechanics, BlockCypherWebhookHandler
from core.utils import to_objectid

from config import BTC_HOT_WALLET_ADDRESS

__all__ = ["invoices_router"]

invoices_router = APIRouter()


@invoices_router.get(
    "/",
    response_model=List[InvoiceInDB],
)
async def admin_invoices_fetch_all(
        status: Optional[Literal[InvoiceStatus.ALL]] = Query(default=None),  # noqa
        invoice_type: Optional[Literal[str(InvoiceType.BUY.value), str(InvoiceType.SELL.value)]] = Query(default=None),
        user_id: Optional[str] = Query(default=None),
):
    q = []
    if status:
        q.append({"status": status})
    if invoice_type:
        q.append({"invoice_type": int(invoice_type)})
    if user_id:
        q.append({"user_id": to_objectid(user_id)})

    q = {"$and": q} if q else {}
    return await InvoiceCRUD.find_many(q)


@invoices_router.get(
    "/{invoice_id}/", response_model=InvoiceExtended
)
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


@invoices_router.post(
    "/{invoice_id}/pay/",
)
async def admin_invoice_pay(invoice_id: str = Path(...)):
    invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(invoice_id, raise_404=True))

    meta_manual_payout = await MetaCRUD.find_by_slug(MetaSlugs.MANUAL_PAYOUT)
    if meta_manual_payout["payload"]["is_active"] is True:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "payout mode is auto")

    if invoice.invoice_type != InvoiceType.SELL or invoice.status != InvoiceStatus.PROCESSING:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid invoice to pay")

    hot_wallet_info = await BitcoinWrapper().fetch_address_and_save(BTC_HOT_WALLET_ADDRESS)

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

    return {"success": True}


@invoices_router.post(
    "/{invoice_id}/cancel/",
    response_model=InvoiceInDB
)
async def admin_invoice_cancel(invoice_id: str = Path(...)):
    invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(invoice_id, raise_404=True))

    if invoice.status not in (InvoiceStatus.CREATED, InvoiceStatus.WAITING, InvoiceStatus.PROCESSING):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid invoice status")

    invoice.status = InvoiceStatus.CANCELLED
    await InvoiceCRUD.update_one({"_id": invoice.id}, invoice.dict(include={"status"}))
    await BlockCypherWebhookHandler().delete_webhook(invoice)

    return invoice
