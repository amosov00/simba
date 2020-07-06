from typing import Optional
from datetime import datetime

from pydantic import Field, validator
from passlib.context import CryptContext
from passlib import pwd

from schemas.base import BaseModel, ObjectIdPydantic


class Referral(BaseModel):
    ref1: ObjectIdPydantic = Field(..., alias="_id", title="_id")
    ref2: ObjectIdPydantic = Field(..., alias="_id", title="_id")
    ref3: ObjectIdPydantic = Field(..., alias="_id", title="_id")
    ref4: ObjectIdPydantic = Field(..., alias="_id", title="_id")
    ref5: ObjectIdPydantic = Field(..., alias="_id", title="_id")
    user_id: ObjectIdPydantic = Field(..., alias="_id", title="_id")


class ReferralInDB(Referral):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
