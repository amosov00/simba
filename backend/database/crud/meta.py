from typing import Optional
from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException

from .base import BaseMongoCRUD

__all__ = ["MetaCRUD"]


class MetaCRUD(BaseMongoCRUD):
    collection = "meta"

    @classmethod
    async def find_by_slug(cls, slug: str, raise_404: bool = False, raise_500: bool = False) -> Optional[dict]:
        res = await cls.find_one({"slug": slug})

        if not res and raise_404:
            raise HTTPException(HTTPStatus.NOT_FOUND, "obj not found")

        if not res and raise_500:
            raise ValueError(f"Meta with '{slug}' slug not found")

        return res

    @classmethod
    async def update_by_slug(cls, slug: str, payload: dict, **kwargs):
        return await super().update_or_insert(
            {"slug": slug}, {"slug": slug, "updated_at": datetime.now(), "payload": payload}, **kwargs
        )
