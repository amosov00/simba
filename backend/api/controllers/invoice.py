from typing import List
from http import HTTPStatus
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request, Response
from api.dependencies import get_user

from database.crud import InvoiceCRUD
from schemas.invoice import (
    Invoice,
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceInDB,
    InvoiceStatus
)
from schemas.user import User


__all__ = ["router"]

router = APIRouter()


@router.post("/", response_model=InvoiceInDB)
async def create_invoice(user: User = Depends(get_user), data: InvoiceCreate = Body(...)):
    return await InvoiceCRUD.create_invoice(user, data)


@router.get("/", response_model=List[InvoiceInDB])
async def show_invoices(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoices_by_user_id(user.id)


@router.get("/{invoice_id}/", response_model=InvoiceInDB)
async def show_invoice_by_id(invoice_id: str, user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoice_by_id(invoice_id, user.id)


@router.put("/{invoice_id}/")
async def update_invoice(invoice_id: str, user: User = Depends(get_user), payload: InvoiceUpdate = Body(...)):
    return await InvoiceCRUD.update_invoice(invoice_id, user, payload.dict(exclude_unset=True))


@router.post("/{invoice_id}/cancel/")
async def cancel_invoice(invoice_id: str, user: User = Depends(get_user)):
    return await InvoiceCRUD.update_invoice(invoice_id, user, {"status": InvoiceStatus.CANCELED})


@router.post("/{invoice_id}/confirm/")
async def confirm_invoice(invoice_id: str, user: User = Depends(get_user)):
    return await InvoiceCRUD.update_invoice(invoice_id, user, {"status": InvoiceStatus.WAITING})
