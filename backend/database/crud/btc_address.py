import pymongo

from .base import BaseMongoCRUD


class BTCAddressCRUD(BaseMongoCRUD):
    collection = "btc_address"

    @classmethod
    async def find_by_address(cls, address: str):
        return await cls.find_one({"address": address})

    @classmethod
    async def find_latest(cls, xpub_title: str, path: str):
        return await cls.db[cls.collection].find_one(
            {"cold_wallet_title": xpub_title, "path": {"$regex": path}},
            sort=[("created_at", pymongo.DESCENDING), ("_id", pymongo.DESCENDING)]
        )

    @classmethod
    async def update_or_create(cls, address: str, data: dict):
        return await cls.update_one({"address": address}, data, upsert=True)
