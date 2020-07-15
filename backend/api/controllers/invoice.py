from http import HTTPStatus
from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Body, Response

from api.dependencies import get_user
from core.mechanics import BitcoinWrapper, InvoiceMechanics, BlockCypherWebhookHandler
from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import (
    Invoice,
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceInDB,
    InvoiceExtended,
    InvoiceStatus,
    InvoiceType,
    INVOICE_MODEL_EXCLUDE_FIELDS,
    BlockCypherWebhookEvents,
)
from schemas.user import User

__all__ = ["router"]

router = APIRouter()


@router.post("/", response_model=InvoiceInDB, response_model_exclude=INVOICE_MODEL_EXCLUDE_FIELDS)
async def create_invoice(
    user: User = Depends(get_user), data: InvoiceCreate = Body(...),
):
    invoice = Invoice(user_id=user.id, status=InvoiceStatus.CREATED, invoice_type=data.invoice_type)

    created_invoice = await InvoiceCRUD.create_invoice(invoice)

    if invoice.invoice_type == InvoiceType.BUY:
        created_invoice["target_btc_address"] = await BitcoinWrapper().create_wallet_address(
            created_invoice, user
        )

    return created_invoice


@router.get("/", response_model=List[InvoiceInDB], response_model_exclude=INVOICE_MODEL_EXCLUDE_FIELDS)
async def invoice_fetch_all(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoices_by_user_id(user.id)


@router.get(
    "/{invoice_id}/", response_model=InvoiceExtended, response_model_exclude=INVOICE_MODEL_EXCLUDE_FIELDS
)
async def invoice_fetch_one(invoice_id: str, user: User = Depends(get_user)):
    resp = await InvoiceCRUD.aggregate(
        [
            {"$match": {"_id": ObjectId(invoice_id), "user_id": user.id}},
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


@router.put("/{invoice_id}/")
async def invoice_update(invoice_id: str, user: User = Depends(get_user), payload: InvoiceUpdate = Body(...)):
    invoice = await InvoiceCRUD.find_by_id(invoice_id, raise_404=True)
    invoice = InvoiceInDB(**invoice)

    if invoice.invoice_type == InvoiceType.BUY:
        if payload.target_eth_address and not user.has_address("eth", payload.target_eth_address):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                {"reason": "unconfirmed_eth_address", "message": "eth address must be confirmed"},
            )

    elif invoice.invoice_type == InvoiceType.SELL:
        if payload.target_eth_address and not user.has_address("eth", payload.target_eth_address):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                {"reason": "unconfirmed_eth_address", "message": "eth address must be confirmed"},
            )
        if payload.target_btc_address and not user.has_address("btc", payload.target_btc_address):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                {"reason": "unconfirmed_btc_address", "message": "btc address must be confirmed"},
            )

    return await InvoiceCRUD.update_invoice(
        invoice_id, user, payload, filtering_statuses=(InvoiceStatus.CREATED,)
    )


@router.post(
    "/{invoice_id}/confirm/", response_model=InvoiceInDB, response_model_exclude=INVOICE_MODEL_EXCLUDE_FIELDS
)
async def invoice_confirm(invoice_id: str, user: User = Depends(get_user)):
    invoice = await InvoiceCRUD.find_invoice_safely(invoice_id, user.id)

    if not invoice:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invoice not found or modification is forbidden")

    invoice = InvoiceInDB(**invoice)
    InvoiceMechanics(invoice, user).validate()

    invoice.status = InvoiceStatus.WAITING
    await BlockCypherWebhookHandler().create_webhook(
        invoice=invoice,
        event=BlockCypherWebhookEvents.TX_CONFIMATION,
        wallet_address=invoice.target_btc_address,
    )
    await InvoiceCRUD.update_invoice_not_safe(invoice.id, user.id, {"status": InvoiceStatus.WAITING})
    return invoice
