from typing import AsyncGenerator

from .base import BaseMongoCRUD
import pymongo


class EthereumTransactionCRUD(BaseMongoCRUD):
    collection = "ethblock"

    @classmethod
    async def find(cls, query: dict, options: dict = None):
        return await super().find_many(query=query, options=options)

    @classmethod
    async def find_last_block(cls, query: dict = None, options: dict = None):
        query = query or {}
        return [
            i
            async for i in cls.db[cls.collection]
            .find(filter=query)
            .sort([("blockNumber", pymongo.DESCENDING)])
            .limit(1)
        ]

    @classmethod
    async def update_or_create(cls, transaction_hash: str, log_index: int, payload: dict):
        return await super().update_one(
            query={"transactionHash": transaction_hash, "logIndex": log_index},
            payload=payload,
            upsert=True,
        )
