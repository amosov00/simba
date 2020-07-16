from typing import List, Literal

from fastapi import APIRouter, Query

from config import BTC_COLD_WALLETS
from database.crud import BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD
from schemas import TransparencyTransaction, InvoiceStatus, InvoiceType, Invoice

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
    btc_tx_hashes = await InvoiceCRUD.aggregate([
        {"$match": {
            "$and": [
                {"status": InvoiceStatus.COMPLETED},
                {"invoice_type": InvoiceType.BUY if tx_type == "received" else InvoiceType.SELL}
            ]
        }},
        {"$project": {"_id": 0, "btc_tx_hashes": 1}},
        {"$unwind": "$btc_tx_hashes"},
    ])
    btc_tx_hashes_list = [i["btc_tx_hashes"] for i in btc_tx_hashes] if btc_tx_hashes else None
    btc_txs = await BTCTransactionCRUD.find_many({
        "hash": {"$in": btc_tx_hashes_list}
    }) if btc_tx_hashes_list else []
    return btc_txs
