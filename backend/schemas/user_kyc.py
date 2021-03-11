from typing import Union

from bson import ObjectId

from schemas.base import (
    BaseModel,
    ObjectIdPydantic,
    Field
)

__all__ = ["UserKYC", "UserKYCInDB"]


class UserKYC(BaseModel):
    user_id: ObjectIdPydantic = Field(...)
    result: str = Field(default=None)
    review_status: str = Field(default=None)
    review_data: dict = Field(default={})
    status_data: dict = Field(default={})


class UserKYCInDB(BaseModel):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
