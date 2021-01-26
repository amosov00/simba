from typing import List, Optional, Union

from pydantic import Field, validator

from schemas.base import BaseModel, ObjectIdPydantic, DecimalPydantic
from schemas.user import UserReferralInfo

__all__ = ["Referral", "ReferralInDB", "UserReferralsResponse", "ReferralTransactionUserID", "ReferralTransactionEmail"]


class Referral(BaseModel):
    user_id: Optional[ObjectIdPydantic] = Field(delault=None)
    ref1: Optional[ObjectIdPydantic] = Field(delault=None)
    ref2: Optional[ObjectIdPydantic] = Field(delault=None)
    ref3: Optional[ObjectIdPydantic] = Field(delault=None)
    ref4: Optional[ObjectIdPydantic] = Field(delault=None)
    ref5: Optional[ObjectIdPydantic] = Field(delault=None)


class ReferralInDB(Referral):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class ReferralTransactionUserID(BaseModel):
    transactionHash: str = Field(...)
    amount: Union[DecimalPydantic, int] = Field(...)
    user_id: ObjectIdPydantic = Field(default=None)
    level: int = Field(default=None)


class ReferralTransactionEmail(BaseModel):
    transactionHash: str = Field(...)
    amount: DecimalPydantic = Field(...)
    email: str = Field(default=None)
    level: int = Field(default=None)

    @validator("email")
    def hide_email(cls, v):  # noqa
        if v:
            v = "@".join([v.split("@")[0], "***.***"])
        return v


class UserReferralsResponse(BaseModel):
    referrals: List[UserReferralInfo] = Field(default=[])
    transactions: List[ReferralTransactionEmail] = Field(default=[])
