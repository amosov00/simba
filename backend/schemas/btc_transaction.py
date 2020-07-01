from typing import Union, List, Optional
from datetime import datetime

from pydantic import Field, HttpUrl

from .base import BaseModel, ObjectIdPydantic

__all__ = [
    "BTCTransaction",
    "BTCTransactionInDB",
    "BTCTransactionInputs",
    "BTCTransactionOutputs",
]


class BTCTransactionInputs(BaseModel):
    prev_hash: str = Field(default=None)
    output_value: str = Field(...)
    addresses: List[str] = Field(...)
    age: int = Field(...)


class BTCTransactionOutputs(BaseModel):
    value: int = Field(...)
    addresses: List[str] = Field(...)


class BTCTransaction(BaseModel):
    invoice_id: ObjectIdPydantic = None
    simba_tokens_issued: bool = False
    addresses: List[str] = None
    block_hash: str = None
    block_height: int = None
    block_index: int = None
    hash: str = None
    total: int = None
    fees: int = None
    size: int = None
    relayed_by: str = None
    double_spend: bool = None
    confirmations: int = None
    confidence: int = None
    confirmed: datetime = None
    received: datetime = None
    inputs: List[BTCTransactionInputs] = Field(default=[])
    outputs: List[BTCTransactionOutputs] = Field(default=[])


class BTCTransactionInDB(BTCTransaction):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
