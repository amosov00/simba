from http import HTTPStatus
from datetime import datetime

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

    @classmethod
    async def update_by_slug(cls, slug: str, payload: dict):
        return await super().update_one(
            {"slug": slug}, {"updated_at": datetime.now(), "payload": payload}
        )

    @classmethod
    async def update_or_create_email_to_support_time(cls):
        pass
