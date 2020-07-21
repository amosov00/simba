from typing import Optional
from datetime import datetime

from pydantic import SecretStr

from .base import BaseModel, ObjectIdPydantic, Field

__all__ = ["BTCxPub", "BTCxPubInDB", "BTCxPubUpdate"]


class BTCxPub(BaseModel):
    title: str = Field(...)
    xpub: SecretStr = Field(...)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)


class BTCxPubInDB(BTCxPub):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class BTCxPubUpdate(BaseModel):
    is_active: bool = Field(...)
