from typing import List
from datetime import datetime

from .base import BaseModel, Field

__all__ = ["TransparencyTransaction", "TransparencyTransactionResponse"]


class TransparencyTransaction(BaseModel):
    hash: str = None
    amount: int = 0
    received: datetime = None


class TransparencyTransactionResponse(BaseModel):
    transactions: List[TransparencyTransaction] = Field(default=[])
    total: int = Field(default=0)
