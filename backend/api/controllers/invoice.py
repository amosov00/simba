from typing import List
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request, Response

from api.dependencies import get_user
from database.crud import InvoiceCRUD
from schemas import (
    Invoice,
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceInDB,
    InvoiceStatus,
    InvoiceType,
    InvoiceTransactionManual,
    BlockCypherWebhookEvents,
)
from schemas.user import User
from core.mechanics import BitcoinWrapper, SimbaWrapper, InvoiceValidation

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
async def fetch_invoices(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoices_by_user_id(user.id)


@router.get("/{invoice_id}/", response_model=InvoiceInDB)
async def show_invoice_by_id(invoice_id: str, user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoice_by_id(invoice_id, user.id)


@router.put("/{invoice_id}/")
async def update_invoice(invoice_id: str, user: User = Depends(get_user), payload: InvoiceUpdate = Body(...)):
    res = await InvoiceCRUD.update_invoice(invoice_id, user, payload.dict(exclude_unset=True))
    return True


@router.post("/{invoice_id}/transaction/")
async def update_invoice(
        invoice_id: str,
        user: User = Depends(get_user),
        payload: InvoiceTransactionManual = Body(...)
):
    invoice = await InvoiceCRUD.find_invoice_safely(
        invoice_id,
        user.id,
        statuses=(InvoiceStatus.WAITING, InvoiceStatus.COMPLETED),
    )
    if not invoice:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Invoice not found")

    invoice = InvoiceInDB(**invoice)
    response = {}

    if invoice.invoice_type == InvoiceType.BUY and payload.btc_transaction_hash:
        tx_meta = await BitcoinWrapper().fetch_and_save_transaction(invoice, payload.btc_transaction_hash)
        eth_tx_hash = await SimbaWrapper().issue_tokens_and_save(
            invoice, invoice.target_eth_address, incoming_btc=tx_meta["incoming_btc"], comment=tx_meta["tx_hash"]
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


@router.post("/{invoice_id}/confirm/")
async def confirm_invoice(invoice_id: str, user: User = Depends(get_user)):
    # Validate invoice
    invoice = await InvoiceCRUD.find_invoice_safely(invoice_id, user.id)

    if not invoice:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invoice not found or modification is forbidden")

    invoice = InvoiceValidation(invoice).validate()

    await InvoiceCRUD.update_invoice_not_safe(invoice.id, user.id, {"status": InvoiceStatus.WAITING})

    # await BlockCypherWebhookHandler().create_webhook(
    #     invoice=invoice,
    #     event=BlockCypherWebhookEvents.UNCONFIRMED_TX,
    #     wallet_address=user.btc_address
    # )

    return True


@router.post("/{invoice_id}/cancel/")
async def cancel_invoice(invoice_id: str, user: User = Depends(get_user)):
    return await InvoiceCRUD.update_invoice(invoice_id, user, {"status": InvoiceStatus.CANCELLED})
