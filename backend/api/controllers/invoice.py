from typing import List
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request, Response, BackgroundTasks
from bson import ObjectId

from api.dependencies import get_user
from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import (
    Invoice,
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceInDB,
    InvoiceExtended,
    InvoiceStatus,
    InvoiceType,
    InvoiceTransactionManual,
    INVOICE_MODEL_EXCLUDE_FIELDS,
    BlockCypherWebhookEvents,
)
from schemas.user import User
from core.mechanics import BitcoinWrapper, SimbaWrapper, InvoiceMechanics, BlockCypherWebhookHandler

__all__ = ["router"]

router = APIRouter()


@router.post("/", response_model=InvoiceInDB, response_model_exclude=INVOICE_MODEL_EXCLUDE_FIELDS)
async def create_invoice(
        background_tasks: BackgroundTasks,
        user: User = Depends(get_user),
        data: InvoiceCreate = Body(...),
):
    invoice = Invoice(
        user_id=user.id,
        status=InvoiceStatus.CREATED,
        invoice_type=data.invoice_type,
    )

    if invoice.invoice_type == InvoiceType.SELL:
        invoice.target_eth_address = data.target_eth_address

    created_invoice = await InvoiceCRUD.create_invoice(invoice)

    if invoice.invoice_type == InvoiceType.BUY:
        background_tasks.add_task(BitcoinWrapper().create_wallet_address, created_invoice)

    return created_invoice


@router.get("/", response_model=List[InvoiceInDB], response_model_exclude=INVOICE_MODEL_EXCLUDE_FIELDS)
async def invoice_fetch_all(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoices_by_user_id(user.id)


@router.get("/{invoice_id}/", response_model=InvoiceExtended, response_model_exclude=INVOICE_MODEL_EXCLUDE_FIELDS)
async def invoice_fetch_one(invoice_id: str, user: User = Depends(get_user)):
    resp = await InvoiceCRUD.aggregate([
        {"$match": {
            "_id": ObjectId(invoice_id),
            "user_id": user.id
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
    return resp[0] if resp else Response(status_code=404)


@router.put("/{invoice_id}/")
async def invoice_update(invoice_id: str, user: User = Depends(get_user), payload: InvoiceUpdate = Body(...)):
    return await InvoiceCRUD.update_invoice(
        invoice_id, user, payload, statuses=(InvoiceStatus.CREATED,),
    )


@router.post("/{invoice_id}/transaction/")
async def invoice_add_transaction(
        invoice_id: str,
        user: User = Depends(get_user),
        payload: InvoiceTransactionManual = Body(...)
):
    invoice = await InvoiceCRUD.find_invoice_safely(
        invoice_id,
        user.id,
        statuses=(InvoiceStatus.WAITING, InvoiceStatus.COMPLETED),
    )

    invoice = InvoiceInDB(**invoice)
    response = {}

    if invoice.invoice_type == InvoiceType.BUY and payload.btc_transaction_hash:
        btc_transaction = await BitcoinWrapper().fetch_transaction(invoice, payload.btc_transaction_hash)
        if not btc_transaction:
            raise HTTPException(HTTPStatus.NOT_FOUND, "transation is not found")

        invoice_mechanics = InvoiceMechanics(invoice)
        invoice_mechanics.validate()
        await invoice_mechanics.proceed_new_transaction(btc_transaction)

        response.update({
            "success": True,
        })

    elif invoice.invoice_type == InvoiceType.SELL and payload.eth_transaction_hash:
        pass

    else:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Payload doesn't match invoice type")

    return response


@router.post("/{invoice_id}/confirm/", response_model=InvoiceInDB, response_model_exclude=INVOICE_MODEL_EXCLUDE_FIELDS)
async def invoice_confirm(invoice_id: str, user: User = Depends(get_user)):
    invoice = await InvoiceCRUD.find_invoice_safely(invoice_id, user.id)

    if not invoice:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invoice not found or modification is forbidden")

    invoice = InvoiceInDB(**invoice)
    InvoiceMechanics(invoice).validate()

    invoice.status = InvoiceStatus.WAITING
    await InvoiceCRUD.update_invoice_not_safe(invoice.id, user.id, {"status": InvoiceStatus.WAITING})
    await BlockCypherWebhookHandler().create_webhook(
        invoice=invoice,
        event=BlockCypherWebhookEvents.TX_CONFIMATION,
        wallet_address=invoice.target_btc_address
    )
    return invoice


# TODO update_invoice was change, need to refactor it
@router.post("/{invoice_id}/cancel/")
async def invoice_cancel(invoice_id: str, user: User = Depends(get_user)):
    await InvoiceCRUD.update_invoice_not_safe(ObjectId(invoice_id), user.id, {"status": InvoiceStatus.CANCELLED})
    return True
