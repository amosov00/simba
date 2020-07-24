import pymongo

from .base import BaseMongoCRUD


__all__ = ['MetaCRUD']

class MetaCRUD(BaseMongoCRUD):
    collection = "meta"

    @classmethod
    async def find_by_slug(cls, slug: str):
        return await cls.find_one({"slug": slug})

