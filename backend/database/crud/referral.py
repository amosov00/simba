from typing import Union, Optional

from bson import ObjectId
from sentry_sdk import capture_message

from database.crud.base import BaseMongoCRUD
from schemas import ReferralInDB

__all__ = ["ReferralCRUD"]


class ReferralCRUD(BaseMongoCRUD):
    collection: str = "referral"

    @classmethod
    async def find_by_user_id(cls, user_id: Union[str, ObjectId]) -> Optional[dict]:
        return await cls.find_one(query={"user_id": ObjectId(user_id)}) if user_id else None

    @classmethod
    async def add_referral(cls, user_id: ObjectId, referral_id: ObjectId):
        referral_obj = await cls.find_by_user_id(referral_id)

        if not referral_obj:
            capture_message("Referral obj is not found")
            return False

        referral_obj = ReferralInDB(**referral_obj)

        return await super().insert_one(
            {
                "user_id": user_id,
                "ref1": referral_id,
                "ref2": referral_obj.ref1,
                "ref3": referral_obj.ref2,
                "ref4": referral_obj.ref3,
                "ref5": referral_obj.ref4,
            }
        )
