from typing import Literal, Union, Tuple

from schemas import (
    Invoice,
    InvoiceStatus,
    InvoiceType,
    InvoiceCreate,
    InvoiceInDB,
    InvoiceUpdate
)
from .base import BaseMongoCRUD, ObjectId
from schemas import User, ObjectIdPydantic
from fastapi.exceptions import HTTPException
from http import HTTPStatus

__all__ = ["InvoiceCRUD"]


class InvoiceCRUD(BaseMongoCRUD):
    collection = "invoice"

    @classmethod
    async def find_invoices_by_type_and_status(
            cls,
            invoice_type: Literal[InvoiceType.BUY, InvoiceType.SELL],
            status: Literal[InvoiceStatus.ALL],  # noqa
    ):
        return await super().find_many({"status": status, "invoice_type": invoice_type})

    @classmethod
    async def find_invoices_by_user_id(cls, user_id: Union[ObjectId, ObjectIdPydantic]):
        return await super().find_many({"user_id": user_id})

    @classmethod
    async def find_invoice_by_id(cls, invoice_id: Union[str, ObjectId], user_id: Union[ObjectId, ObjectIdPydantic]):
        return await super().find_one({
            "_id": ObjectId(invoice_id),
            "user_id": user_id
        })

    @classmethod
    async def find_invoice_safely(
            cls,
            invoice_id: str,
            user_id: Union[ObjectId, ObjectIdPydantic],
            statuses: tuple = (InvoiceStatus.CREATED, )
    ):
        return await super().find_one({
            "_id": ObjectId(invoice_id),
            "user_id": user_id,
            "status": {"$in": list(statuses)}
        })

    @classmethod
    async def invoice_info(cls, invoice_id: str, user: User):
        pass

    @classmethod
    async def create_invoice(cls, data: Invoice) -> dict:
        inserted_id = (await super().insert_one(data.dict())).inserted_id
        created_invoice = await cls.find_one(query={"_id": inserted_id})
        return created_invoice

    @classmethod
    async def update_invoice(cls, invoice_id: str, user: User, payload: dict):
        if not payload:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Payload is required")

        invoice = await cls.find_invoice_safely(invoice_id, user.id)
        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Invoice not found or modification is forbidden")

        await cls.update_one(
            query={
                "user_id": user.id,
                "_id": invoice["_id"],
            },
            payload=payload,
        )
        return {**invoice, **payload}

    @classmethod
    async def update_invoice_not_safe(
            cls,
            invoice_id: Union[ObjectId, ObjectIdPydantic],
            user_id: Union[ObjectId, ObjectIdPydantic],
            payload: dict
    ) -> bool:
        return await super().update_one({"_id": invoice_id, "user_id": user_id}, payload)
