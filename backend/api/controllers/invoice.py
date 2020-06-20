from typing import List
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request, Response
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
    BlockCypherWebhookEvents,
)
from schemas.user import User
from core.mechanics import BitcoinWrapper, SimbaWrapper, InvoiceMechanics, BlockCypherWebhookHandler

__all__ = ["router"]

router = APIRouter()


@router.post("/", response_model=InvoiceInDB, response_model_exclude={"validation_md5_hash"})
async def create_invoice(user: User = Depends(get_user), data: InvoiceCreate = Body(...)):
    invoice = Invoice(
        user_id=user.id,
        status=InvoiceStatus.CREATED,
        invoice_type=data.invoice_type,
    )
    if invoice.invoice_type == InvoiceType.BUY:
        invoice.target_btc_address = user.btc_address
    elif invoice.invoice_type == InvoiceType.SELL:
        pass

    return await InvoiceCRUD.create_invoice(invoice)


@router.get("/", response_model=List[InvoiceInDB])
async def invoice_fetch_all(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoices_by_user_id(user.id)


@router.get("/{invoice_id}/", response_model=InvoiceExtended)
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
        # TODO return full tx
        tx_meta = await BitcoinWrapper().fetch_and_save_transaction(invoice, payload.btc_transaction_hash)
        # TOOD Has no validation if transaction already exists
        # TODO refactor -> to InvoiceMechanics
        eth_tx_hash = await SimbaWrapper().validate_and_issue_tokens(
            invoice, incoming_btc=tx_meta["incoming_btc"], comment=tx_meta["tx_hash"]
        )
        response.update({
            "success": True,
            "tx_hash": eth_tx_hash,
        })

    elif invoice.invoice_type == InvoiceType.SELL and payload.eth_transaction_hash:
        pass

    else:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Payload doesn't match invoice type")

    return response


@router.post("/{invoice_id}/confirm/", response_model=InvoiceInDB)
async def invoice_confirm(invoice_id: str, user: User = Depends(get_user)):
    invoice = await InvoiceCRUD.find_invoice_safely(invoice_id, user.id)

    if not invoice:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invoice not found or modification is forbidden")

    invoice = InvoiceMechanics(invoice).validate()

    invoice.status = InvoiceStatus.WAITING
    await InvoiceCRUD.update_invoice_not_safe(invoice.id, user.id, {"status": InvoiceStatus.WAITING})

    await BlockCypherWebhookHandler().create_webhook(
        invoice=invoice,
        event=BlockCypherWebhookEvents.TX_CONFIMATION,
        wallet_address=user.btc_address
    )
    return invoice

# TODO update_invoice was change, need to refactor it
# @router.post("/{invoice_id}/cancel/")
# async def invoice_cancel(invoice_id: str, user: User = Depends(get_user)):
#     return await InvoiceCRUD.update_invoice(invoice_id, user, {"status": InvoiceStatus.CANCELLED})
