from typing import AsyncGenerator

from .base import BaseMongoCRUD
import pymongo


class EthereumTransactionCRUD(BaseMongoCRUD):
    collection = "ethblock"

    @classmethod
    async def find(cls, query: dict, options: dict = None):
        return await super().find_many(query=query, options=options)

    @classmethod
    async def find_last_block(cls):
        return await cls.db[cls.collection].find_one({}, sort=[("blockNumber", pymongo.DESCENDING)])

    @classmethod
    async def update_or_create(cls, transaction_hash: str, log_index: int, payload: dict):
        return await super().update_one(
            query={"transactionHash": transaction_hash, "logIndex": log_index}, payload=payload, upsert=True,
        )
