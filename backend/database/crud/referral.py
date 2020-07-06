from typing import Union, Optional, List
from http import HTTPStatus

from bson import ObjectId
from sentry_sdk import capture_message
from fastapi import HTTPException

from schemas import ReferralInDB
from database.crud.base import BaseMongoCRUD
from core.utils import to_objectid

__all__ = ["ReferralCRUD"]


class ReferralCRUD(BaseMongoCRUD):
    collection: str = "referral"

    @classmethod
    async def find_by_user_id(cls, _id: Union[str, ObjectId]) -> Optional[dict]:
        return await super().find_one(query={"user_id": to_objectid(_id)}) if _id else None

    @classmethod
    async def add_referral(cls, user_id: ObjectId, referral_id: ObjectId):
        referral_obj = await cls.find_by_user_id(referral_id)

        if not referral_obj:
            capture_message("Referral obj is not found")

        referral_obj = ReferralInDB(**referral_obj) if referral_obj else None

        return await super().insert_one(
            {
                "user_id": user_id,
                "ref1": referral_id,
                "ref2": referral_obj.ref1 if referral_obj else None,
                "ref3": referral_obj.ref2 if referral_obj else None,
                "ref4": referral_obj.ref3 if referral_obj else None,
                "ref5": referral_obj.ref4 if referral_obj else None,
            }
        )
