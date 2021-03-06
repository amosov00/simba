from http import HTTPStatus
from typing import Literal, Union

from bson import ObjectId, errors
from fastapi.exceptions import HTTPException

from schemas import (
    Invoice,
    InvoiceStatus,
    InvoiceType,
    InvoiceUpdate,
    User,
    ObjectIdPydantic,
)
from .base import BaseMongoCRUD
from .btc_transaction import BTCTransactionCRUD
from .eth_transaction import EthereumTransactionCRUD

__all__ = ["InvoiceCRUD"]


class InvoiceCRUD(BaseMongoCRUD):
    collection = "invoice"

    @classmethod
    async def find_invoices_by_type_and_status(
        cls,
        invoice_type: Literal[InvoiceType.BUY, InvoiceType.SELL],  # noqa
        status: Literal[InvoiceStatus.ALL],  # noqa
    ):
        return await super().find_many({"status": status, "invoice_type": invoice_type})

    @classmethod
    async def find_invoices_by_user_id(cls, user_id: Union[ObjectId, ObjectIdPydantic]):
        return await super().find_many({"user_id": user_id})

    @classmethod
    async def find_invoice_by_id(
        cls,
        invoice_id: Union[str, ObjectId],
        user_id: Union[ObjectId, ObjectIdPydantic],
    ):
        return await super().find_one({"_id": ObjectId(invoice_id), "user_id": user_id})

    @classmethod
    async def find_invoice_safely(
        cls,
        invoice_id: str,
        user_id: Union[ObjectId, ObjectIdPydantic],
        filtering_statuses: tuple = (InvoiceStatus.CREATED,),
    ):
        invoice = await super().find_one(
            {
                "_id": ObjectId(invoice_id),
                "user_id": user_id,
            }
        )
        if not invoice:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Invoice not found")

        if invoice["status"] not in filtering_statuses:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "This operation is not permitted")

        return invoice

    @classmethod
    async def find_by_query(cls, q: str, invoice_type: str = "", invoice_status: str = "") -> list:
        query = []

        if q:
            q_len = len(q)

            if q_len == 24:
                for f in ("_id", "user_id"):
                    try:
                        query.append({f: ObjectId(q)})
                    except errors.InvalidId:
                        pass
            if q_len >= 30:
                for f in ("btc_tx_hashes", "eth_tx_hashes", "sst_tx_hashes", ""):
                    query.append({f: {"$regex": q, "$options": "i"}})

            if q_len == 42:
                query.append({"target_eth_address": {"$regex": q, "$options": "i"}})

            if q_len == 34:
                query.append({"target_btc_address": {"$regex": q, "$options": "i"}})

        if invoice_type:
            query.append({"invoice_type": int(invoice_type)})

        if invoice_status:
            query.append({"status": invoice_status})

        query = {"$or": query} if query else {}
        return await super().find_many(query)

    @classmethod
    async def create_invoice(cls, data: Invoice) -> dict:
        inserted_id = (await super().insert_one(data.dict())).inserted_id
        return await cls.find_one(query={"_id": inserted_id})

    @classmethod
    async def update_invoice(
        cls, invoice_id: str, user: User, payload: InvoiceUpdate, filtering_statuses: tuple = None
    ):
        if not payload.dict(exclude_unset=True):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Payload is required")

        invoice = await cls.find_invoice_safely(invoice_id, user.id, filtering_statuses)

        if invoice["invoice_type"] == InvoiceType.BUY:
            payload = payload.dict(exclude={"target_btc_address"}, exclude_unset=True)
        elif invoice["invoice_type"] == InvoiceType.SELL:
            payload = payload.dict(exclude_unset=True)

        await cls.update_one(
            query={"user_id": user.id, "_id": invoice["_id"]},
            payload=payload,
        )
        return True

    @classmethod
    async def update_invoice_not_safe(
        cls,
        invoice_id: Union[ObjectId, ObjectIdPydantic],
        user_id: Union[ObjectId, ObjectIdPydantic],
        payload: dict,
    ) -> bool:
        return await super().update_one({"_id": invoice_id, "user_id": user_id}, payload)

    @classmethod
    async def update_invoice_admin(
        cls, invoice_id: Union[ObjectId, ObjectIdPydantic], payload: dict, filtering_statuses: tuple = None
    ):
        query = {"_id": invoice_id}

        if filtering_statuses:
            query.update({"status": {"$in": filtering_statuses}})

        return await super().update_one(query, payload)

    @classmethod
    async def need_to_update(
        cls,
        invoice_id: Union[ObjectId, ObjectIdPydantic],
        user: User,
        payload: InvoiceUpdate,
    ):
        invoice = await cls.find_by_id(ObjectId(invoice_id))
        if invoice is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid invoice id")
        if invoice["invoice_type"] == InvoiceType.BUY:
            if payload.target_eth_address is not None and user.user_eth_addresses == []:
                return True
            else:
                return False
        return False

    @classmethod
    async def find_with_txs(cls, match_query: dict = None, fetch_btc: bool = True, fetch_eth: bool = True, **kwargs):
        pipeline = [{"$match": match_query}]

        if fetch_btc:
            pipeline.append(
                {
                    "$lookup": {
                        "from": BTCTransactionCRUD.collection,
                        "localField": "_id",
                        "foreignField": "invoice_id",
                        "as": "btc_txs",
                    }
                }

            )

        if fetch_eth:
            pipeline.append(
                {
                    "$lookup": {
                        "from": EthereumTransactionCRUD.collection,
                        "localField": "_id",
                        "foreignField": "invoice_id",
                        "as": "eth_txs",
                    }
                },
            )

        return await super().aggregate(pipeline, **kwargs)
