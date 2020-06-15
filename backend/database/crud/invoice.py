from typing import Literal

from schemas import InvoiceStatus, InvoiceType
from .base import BaseMongoCRUD, ObjectId


class InvoiceCRUD(BaseMongoCRUD):
    collection = "invoice"

    @classmethod
    async def find_invoices_by_type_and_status(
            cls,
            invoice_type: Literal[InvoiceType.BUY, InvoiceType.SELL],
            status: Literal[InvoiceStatus.ALL]  # noqa
    ):
        return await cls.find_many({"status": status})

    @classmethod
    async def find_invoices_by_user_id(cls, user_id: ObjectId):
        return await cls.find_many({"user_id": user_id})
