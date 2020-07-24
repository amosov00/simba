from datetime import datetime

from .base import BaseModel, ObjectIdPydantic, Field

__all__ = ["Meta", "MetaInDB"]


class Meta(BaseModel):
    slug: str = Field(...)
    payload: dict = Field(...)
    updated_at: datetime = Field(default_factory=datetime.now)


class MetaInDB(Meta):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
