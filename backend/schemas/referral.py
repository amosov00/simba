from typing import Optional
from datetime import datetime

from pydantic import Field, validator
from passlib.context import CryptContext
from passlib import pwd

from schemas.base import BaseModel, ObjectIdPydantic


class Referral(BaseModel):
    user_id: Optional[ObjectIdPydantic] = Field(delault=None)
    ref1: Optional[ObjectIdPydantic] = Field(delault=None)
    ref2: Optional[ObjectIdPydantic] = Field(delault=None)
    ref3: Optional[ObjectIdPydantic] = Field(delault=None)
    ref4: Optional[ObjectIdPydantic] = Field(delault=None)
    ref5: Optional[ObjectIdPydantic] = Field(delault=None)


class ReferralInDB(Referral):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
