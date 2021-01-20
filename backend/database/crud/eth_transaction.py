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

    @classmethod
    async def update_or_create(cls, transaction_hash: str, log_index: int, payload: dict):
        return await super().update_one(
            query={"transactionHash": transaction_hash, "logIndex": log_index},
            payload=payload,
            upsert=True,
        )

    @classmethod
    async def find_one_or_insert(cls, query: dict, payload: dict):
        if not await super().find_one(query):
            await super().insert_one(payload)

        return True
