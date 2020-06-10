from typing import Union, List, Optional
from datetime import datetime

from pydantic import Field, HttpUrl

from .base import BaseModel, ObjectIdPydantic

__all__ = [
    "BTCAddress",
    "BTCAddressInDB",
    "BTCAddressTransactions",
]


class BTCAddressTransactions(BaseModel):
    transactions_hash: int = Field(default=0, alias="tx_hash")
    block_height: int = Field(...)
    value: int = Field(...)
    ref_balance: int = Field(...)
    confirmations: int = Field(...)
    confirmed: datetime = Field(...)


class BTCAddress(BaseModel):
    user_id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    address: str = Field(...)
    public_key: str = Field(default=None)
    path: str = Field(default=None)
    balance: int = Field(...)
    total_received: int = Field(...)
    total_sent: int = Field(...)
    transactions_refs: List[BTCAddressTransactions] = Field(...)
    transactions_number: int = Field(default=0, alias="n_tx")
    url: HttpUrl = Field(default=None, alias="tx_url")


class BTCAddressInDB(BTCAddress):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")

