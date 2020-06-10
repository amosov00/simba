from typing import Union, List, Optional
from datetime import datetime

from pydantic import Field, HttpUrl

from .base import BaseModel, ObjectIdPydantic

__all__ = [
    "BTCTransaction",
    "BTCTransactionInDB",
    "BTCTransactionRecipient",
    "BTCTransactionSender",
]


class BTCTransactionSender(BaseModel):
    prev_hash: str = Field(default=None)
    output_value: str = Field(...)
    addresses: List[str] = Field(...)
    age: int = Field(...)


class BTCTransactionRecipient(BaseModel):
    value: int = Field(...)
    addresses: List[str] = Field(...)


class BTCTransaction(BaseModel):
    block_hash: str = None
    block_height: str = None
    block_index: str = None
    hash: str = None
    total: int = None
    fee: int = None
    size: int = None
    confirmations: int = None
    confidence: int = None
    confirmed: datetime = None
    received: datetime = None
    senders: List[BTCTransactionSender] = Field(...)
    recipients: List[BTCTransactionRecipient] = Field(...)
    recipient_address: str = Field(default=None)
    sender_address: str = Field(default=None)


class BTCTransactionInDB(BTCTransaction):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
