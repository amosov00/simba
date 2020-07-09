from typing import Union

import pymongo

from schemas.base import ObjectIdPydantic
from .base import BaseMongoCRUD, ObjectId


class BTCAddressCRUD(BaseMongoCRUD):
    collection = "btc_address"

    @classmethod
    async def find_by_address(cls, address: str):
        return await cls.find_one({"address": address})

    @classmethod
    async def find_latest(cls):
        return await cls.db[cls.collection].find_one(
            sort=[("created_at", pymongo.DESCENDING), ("_id", pymongo.DESCENDING)]
        )

    @classmethod
    async def update_or_create(cls, _id: Union[ObjectId, ObjectIdPydantic], data: dict):
        return await cls.update_one({"_id": _id}, data, upsert=True)
