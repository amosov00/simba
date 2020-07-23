from typing import Optional, List

from pydantic import Field

from schemas.base import BaseModel, ObjectIdPydantic
from schemas.user import UserReferralInfo

__all__ = ["Referral", "ReferralInDB", "UserReferralsResponse"]


class Referral(BaseModel):
    user_id: Optional[ObjectIdPydantic] = Field(delault=None)
    ref1: Optional[ObjectIdPydantic] = Field(delault=None)
    ref2: Optional[ObjectIdPydantic] = Field(delault=None)
    ref3: Optional[ObjectIdPydantic] = Field(delault=None)
    ref4: Optional[ObjectIdPydantic] = Field(delault=None)
    ref5: Optional[ObjectIdPydantic] = Field(delault=None)


class ReferralInDB(Referral):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class ReferralTransaction(BaseModel):
    transactionHash: str = Field(...)
    amount: int = Field(...)
    email: str = Field(default=None)
    level: int = Field(default=None)


class UserReferralsResponse(BaseModel):
    referrals: List[UserReferralInfo] = Field(default=[])
    transactions: List[ReferralTransaction] = Field(default=[])
