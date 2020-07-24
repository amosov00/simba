from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException

from .base import BaseMongoCRUD
from schemas import BTCxPubUpdate

__all__ = ['BTCxPubCRUD']


class BTCxPubCRUD(BaseMongoCRUD):
    collection = "btc_xpub"

    @classmethod
    async def find_by_title(cls, title: str):
        return await cls.find_one({"title": title})

    @classmethod
    async def find_active(cls):
        return await super().find_many({"is_active": True})

    @classmethod
    async def update(cls, xpub_id: str, payload: BTCxPubUpdate) -> bool:
        xpub_in_db = await super().find_by_id(xpub_id, raise_404=True)

        if len(await cls.find_active()) <= 1 and payload.is_active is False:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "at least 1 xpub must be active")

        modified_count = (await super().update_one(
            {"_id": xpub_in_db["_id"]},
            {
                **payload.dict(),
                "updated_at": datetime.now()
            }
        )).modified_count

        return bool(modified_count)
