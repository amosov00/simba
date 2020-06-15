from typing import Literal

from schemas import (
    InvoiceStatus,
    InvoiceType,
    InvoiceCreate,
    InvoiceInDB,
    InvoiceCreateRequest,
    InvoiceUpdate
)
from .base import BaseMongoCRUD, ObjectId
from schemas.user import User
from fastapi.exceptions import HTTPException
from http import HTTPStatus

__all__ = ["InvoiceCRUD"]


class InvoiceCRUD(BaseMongoCRUD):
    collection = "invoices"

    @classmethod
    async def find_invoices_by_type_and_status(
        cls,
        invoice_type: Literal[InvoiceType.BUY, InvoiceType.SELL],
        status: Literal[InvoiceStatus.ALL],  # noqa
    ):
        return await cls.find_many({"status": status})

    @classmethod
    async def find_invoices_by_user_id(cls, user_id: ObjectId):
        return await cls.find_many({"user_id": user_id})

    @classmethod
    async def find_invoice_by_id(cls, invoice_id: str, user_id: ObjectId):
        return await cls.find_one({
            "_id": ObjectId(invoice_id),
            "user_id": user_id
        })

    @classmethod
    async def create_invoice(cls, user: User, data: InvoiceCreateRequest):
        user_id = user.id
        inserted_id = (
            await cls.insert_one(
                payload={
                    **data.dict(),
                    "user_id": user_id,
                    "invoice_type": data.invoice_type,
                    "status": InvoiceStatus.CREATED,
                }
            )
        ).inserted_id
        created_invoice = await cls.find_one(query={"_id": inserted_id})
        return created_invoice

    @classmethod
    async def update_invoice(cls, invoice_id: str, user_id: ObjectId, payload: InvoiceUpdate):
        if not invoice_id or not await cls.find_invoice_by_id(ObjectId(invoice_id), user_id):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "No such invoice",
            )
        try:
            await cls.update_one(
                query={
                    "user_id": user_id,
                    "_id": ObjectId(invoice_id)
                },
                payload=payload.dict(exclude_unset=True),
            )
        except Exception:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "Error while updating invoice",
            )
        return True
