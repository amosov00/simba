import asyncio
from datetime import datetime

from database.crud import BTCAddressCRUD
from config import BTC_HOT_WALLET_ADDRESS


async def main():
    btc_addresses = await BTCAddressCRUD.aggregate([
        {"$match": {"address": {"$ne": BTC_HOT_WALLET_ADDRESS}}},
        {"$group": {"_id": "$address", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": 2}}}
    ])
    btc_addresses = [i["_id"] for i in btc_addresses]
    btc_objs = await BTCAddressCRUD.find_many({
        "address": {"$in": btc_addresses}, "path": None, "created_at": {"$lte": datetime(2020, 1, 2, 0, 0)}
    })
    for obj in btc_objs:
        await BTCAddressCRUD.delete_one({"_id": obj["_id"]})

    print(f"Deleted {len(btc_objs)}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
