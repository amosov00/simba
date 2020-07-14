from typing import List
from fastapi import APIRouter

from database.crud import BTCAddressCRUD
from schemas import TransparencyTransaction
from config import BTC_COLD_XPUB_SWISS, BTC_COLD_XPUB_UAE, BTC_COLD_XPUB_NEWZEL, BTC_COLD_XPUB_LIECH, \
    BTC_COLD_WALLETS, BTC_HOT_WALLET_ADDRESS

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def transparency_totals():
    response = {}
    cold_wallets_meta = await BTCAddressCRUD.aggregate([
        {"$group": {
            "_id": "$cold_wallet_title",
            "received": {"$sum": "$total_received"},
        }}
    ])
    hot_wallet_meta = await BTCAddressCRUD.find_one({"address": BTC_HOT_WALLET_ADDRESS})
    total_recieved = sum([i["received"] for i in cold_wallets_meta if i["_id"]]) or 0
    total_paid_out = hot_wallet_meta.get("total_sent") or 0
    response.update({
        "total_assets": total_recieved - total_paid_out,
        "total_recieved": total_recieved,
        "total_paid_out": total_paid_out,
    })

    for cold_wallet in BTC_COLD_WALLETS:
        meta = list(filter(lambda o: o["_id"] == cold_wallet.title, cold_wallets_meta))
        received = meta[0].get("received") if meta else 0
        response.update({
            cold_wallet.title: {"received": received}
        })

    return response


@router.get("/transactions/", response_model=List[TransparencyTransaction])
async def transparency_transactions():
    transactions = await BTCAddressCRUD.aggregate([
        {"$match": {"cold_wallet_title": {"$in": [i.title for i in BTC_COLD_WALLETS]}}},
        {"$project": {"_id": 0, "transactions_refs": 1}},
        {"$unwind": "$transactions_refs"},
        {"$sort": {"transactions_refs.confirmed": -1}}
    ])
    return [i["transactions_refs"] for i in transactions]
