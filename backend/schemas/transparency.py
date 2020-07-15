from datetime import datetime

from .base import BaseModel

__all__ = ["TransparencyTransaction"]


class TransparencyTransaction(BaseModel):
    transactions_hash: str = None
    value: str = None
    confirmed: datetime = None

    class Config:
        json_encoders = {
            datetime: lambda o: o.timestamp(),
        }
