from datetime import datetime

from .base import BaseModel

__all__ = ["TransparencyTransaction"]


class TransparencyTransaction(BaseModel):
    hash: str = None
    amount: int = 0
    received: datetime = None
