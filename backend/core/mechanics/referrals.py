from typing import List

from database.crud import UserCRUD, ReferralCRUD
from schemas import User

__all__ = ["ReferralMechanics"]


class ReferralMechanics:
    def __init__(self, user: User):
        self.user = user
        self.referrals: List[dict] = []
        self.referrals_transactions: List[dict] = []

    async def fetch_referrals_transactions(self):
        pass

    async def fetch_referrals(self) -> list:
        for ref_level in range(1, 6):
            ref_objects = await ReferralCRUD.find_many({f"ref{ref_level}": self.user.id})
            users_ids = [i["user_id"] for i in ref_objects]

            if users_ids:
                users = await UserCRUD.aggregate(
                    [{"$match": {"_id": {"$in": users_ids}}}, {"$addFields": {"referral_level": ref_level}},]
                )
                self.referrals.extend(users)

        return self.referrals
