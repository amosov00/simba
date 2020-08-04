from typing import Optional
from datetime import datetime

from pydantic import SecretStr, validator

from .base import BaseModel, ObjectIdPydantic, Field

__all__ = ["BTCxPub", "BTCxPubInDB", "BTCxPubUpdate"]


class BTCxPub(BaseModel):
    title: str = Field(...)
    xpub: SecretStr = Field(default=None)
    xpub_preview: str = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)

    @validator("xpub_preview", pre=True)
    def format_xpub_preview(cls, v, values):
        if not values.get("xpub"):
            return ""

        else:
            prefix = values["xpub"].get_secret_value()[:4]
            xpub = values["xpub"].get_secret_value()[-4:]

        assert len(xpub) == 4 and len(prefix) == 4

        return f"{prefix}...{xpub}"


class BTCxPubInDB(BTCxPub):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class BTCxPubUpdate(BaseModel):
    is_active: bool = Field(...)
