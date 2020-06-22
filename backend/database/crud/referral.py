from typing import Union, Optional, List

from database.crud.base import BaseMongoCRUD
from core.utils import to_objectid


__all__ = ["ReferralCRUD"]


class ReferralCRUD(BaseMongoCRUD):
    collection: str = "referrals"

    @classmethod
    async def find_by_user_id(cls, _id: str) -> Optional[dict]:
        return (
            await super().find_one(query={"user_id": to_objectid(_id)}) if _id else None
        )

    @classmethod
    async def add_referral(cls, new_user_id: str, ref_user_id: str):

        referral = await cls.find_by_user_id(ref_user_id)

        inserted_id = (
            await cls.insert_one(
                payload={
                    "user_id": new_user_id,
                    "ref1": ref_user_id,
                    "ref2": referral["ref1"] if (referral and "ref1" in referral) else None,
                    "ref3": referral["ref2"] if (referral and "ref2" in referral) else None,
                    "ref4": referral["ref3"] if (referral and "ref3" in referral) else None,
                    "ref5": referral["ref4"] if (referral and "ref4" in referral) else None
                }
            )
        ).inserted_id

        return inserted_id
