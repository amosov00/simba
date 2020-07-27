from http import HTTPStatus

from fastapi import HTTPException
from .base import BaseMongoCRUD

__all__ = ['MetaCRUD']


class MetaCRUD(BaseMongoCRUD):
    collection = "meta"

    @classmethod
    async def find_by_slug(cls, slug: str, raise_404: bool = True):
        res = await cls.find_one({"slug": slug})

        if not res and raise_404:
            raise HTTPException(HTTPStatus.NOT_FOUND, "obj not found")

        return res
