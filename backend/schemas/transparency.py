from datetime import datetime

from .base import BaseModel

__all__ = ["TransparencyTransaction"]


class TransparencyTransaction(BaseModel):
    hash: str = None
    value: int = 0
    confirmed: datetime = None

    class Config:
        json_encoders = {
            datetime: lambda o: int(o.timestamp()),
        }
