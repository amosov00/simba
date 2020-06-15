from typing import List
from http import HTTPStatus
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request, Response
from api.dependencies import get_user

from database.crud import InvoiceCRUD
from schemas.invoice import (
    Invoice,
    InvoiceCreate,
    InvoiceCreateRequest,
    InvoiceCreateResponse,
    InvoiceUpdate

)
from schemas.user import User


__all__ = ["router"]

router = APIRouter()


@router.post("/", response_model=InvoiceCreateResponse)
async def create_invoice(user: User = Depends(get_user), data: InvoiceCreateRequest = Body(...)):
    return await InvoiceCRUD.create_invoice(user, data)


@router.get("/", response_model=List[Invoice])
async def show_invoices(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoices_by_user_id(user.id)


@router.get("/{invoice_id}/", response_model=Invoice)
async def show_invoice_by_id(invoice_id: str, user: User = Depends(get_user)):
    return await InvoiceCRUD.find_invoice_by_id(invoice_id, user.id)


@router.put("/{invoice_id}/")
async def update_invoice(invoice_id: str, user: User = Depends(get_user), payload: InvoiceUpdate = Body(...)):
    resp = await InvoiceCRUD.update_invoice(invoice_id, user.id, payload) if payload.dict(exclude_unset=True) else {}
    return resp

