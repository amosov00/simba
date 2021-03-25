import pymongo

from .base import BaseMongoCRUD


class EthereumTransactionCRUD(BaseMongoCRUD):
    collection = "ethblock"

    @classmethod
    async def find(cls, query: dict):
        return await super().find_many(query)

    @classmethod
    async def find_last_block(cls, contract_title: str = None):
        q = {"contract": contract_title} if contract_title else {}
        return await cls.db[cls.collection].find_one(q, sort=[("blockNumber", pymongo.DESCENDING)])
