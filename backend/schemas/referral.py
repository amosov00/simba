from typing import Optional, List

from pydantic import Field

from schemas.base import BaseModel, ObjectIdPydantic
from schemas.user import UserReferralInfo
from schemas.eth_transaction import EthereumTransactionReferral

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


class UserReferralsResponse(BaseModel):
    referrals: List[UserReferralInfo] = Field(default=[])
    transactions: List[EthereumTransactionReferral] = Field(default=[])
