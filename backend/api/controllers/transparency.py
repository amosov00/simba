from typing import List, Literal

from fastapi import APIRouter, Query

from config import BTC_COLD_WALLETS
from database.crud import BTCAddressCRUD, InvoiceCRUD
from schemas import TransparencyTransaction, InvoiceStatus, InvoiceType

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def transparency_totals():
    response = {}
    cold_wallets_meta = await BTCAddressCRUD.aggregate(
        [{"$group": {"_id": "$cold_wallet_title", "received": {"$sum": "$total_received"}, }}]
    )
    invoices_meta = await InvoiceCRUD.aggregate(
        [
            {"$match": {"status": InvoiceStatus.COMPLETED, "invoice_type": InvoiceType.SELL}},
            {"$group": {"_id": None, "paid_out": {"$sum": "$btc_amount_proceeded"}}},
        ]
    )
    total_recieved = sum([i["received"] for i in cold_wallets_meta if i["_id"]]) or 0
    total_paid_out = invoices_meta[0].get("paid_out") if invoices_meta else 0
    response.update(
        {
            "total_assets": total_recieved - total_paid_out,
            "total_recieved": total_recieved,
            "total_paid_out": total_paid_out,
        }
    )

    for cold_wallet in BTC_COLD_WALLETS:
        meta = list(filter(lambda o: o["_id"] == cold_wallet.title, cold_wallets_meta))
        received = meta[0].get("received") if meta else 0
        response.update({cold_wallet.title: {"received": received}})

    return response


@router.get("/transactions/", response_model=List[TransparencyTransaction])
async def transparency_transactions(
        tx_type: Literal["received", "paidout"] = Query(default="received", alias="type")
):
    invoices = await InvoiceCRUD.find_many({
        "status": InvoiceStatus.COMPLETED,
        "invoice_type": InvoiceType.BUY if tx_type == "" else InvoiceType.SELL
    }, {"target_btc_address": ""})
    transactions = await BTCAddressCRUD.aggregate(
        [
            {"$match": {
                "cold_wallet_title": {"$in": [i.title for i in BTC_COLD_WALLETS]}},
            },
            {"$project": {"_id": 0, "transactions_refs": 1}},
            {"$unwind": "$transactions_refs"},
            {"$sort": {"transactions_refs.confirmed": -1}},
        ]
    )
    return [i["transactions_refs"] for i in transactions]
