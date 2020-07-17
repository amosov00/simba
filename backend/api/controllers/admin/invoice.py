from typing import List, Literal, Optional
from http import HTTPStatus

from fastapi import APIRouter, Path, Query, Response

from database.crud import InvoiceCRUD, BTCTransactionCRUD, EthereumTransactionCRUD
from schemas import InvoiceInDB, InvoiceExtended, InvoiceStatus, InvoiceType
from core.utils import to_objectid

__all__ = ["invoices_router"]

invoices_router = APIRouter()


@invoices_router.get(
    "/",
    response_model=List[InvoiceInDB],
)
async def admin_invoices_fetch_all(
        status: Optional[Literal[InvoiceStatus.ALL]] = Query(default=None),  # noqa
        invoice_type: Optional[Literal[str(InvoiceType.BUY.value), str(InvoiceType.SELL.value)]] = Query(default=None),  # noqa
        user_id: Optional[str] = Query(default=None),
):
    q = []
    if status:
        q.append({"status": status})
    if invoice_type:
        q.append({"invoice_type": int(invoice_type)})
    if user_id:
        q.append({"user_id": to_objectid(user_id)})

    q = {"$and": q} if q else {}
    return await InvoiceCRUD.find_many(q)


@invoices_router.get(
    "/{invoice_id}/", response_model=InvoiceExtended
)
async def admin_invoice_fetch_one(invoice_id: str = Path(...)):
    resp = await InvoiceCRUD.aggregate(
        [
            {"$match": {"_id": to_objectid(invoice_id)}},
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
