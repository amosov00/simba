from datetime import datetime

from .base import BaseModel, ObjectIdPydantic, Field

__all__ = ["UserAddressesArchive", "UserAddressesArchiveInDB"]


class UserAddressesArchive(BaseModel):
    """
    Is used for storing btc and eth addresses which was deleted
    """
    user_id: ObjectIdPydantic = Field(...)
    address: str = Field(...)
    signature: str = Field(default=None, description="only for eth address")
    deleted_at: datetime = Field(default_factory=datetime.utcnow)


class UserAddressesArchiveInDB(UserAddressesArchive):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
