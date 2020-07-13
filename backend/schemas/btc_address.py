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
    transactions_hash: str = Field(default=0, alias="tx_hash", title="tx_hash")
    block_height: int = Field(...)
    value: int = Field(...)
    ref_balance: int = Field(...)
    confirmations: int = Field(...)
    confirmed: datetime = Field(...)
    double_spend: bool = Field(...)


class BTCAddress(BaseModel):
    user_id: ObjectIdPydantic = Field(default=None)
    invoice_id: ObjectIdPydantic = Field(default=None)
    address: str = Field(...)
    public_key: str = Field(default=None)
    path: str = Field(default=None)
    balance: int = Field(default=0)
    unconfirmed_balance: int = Field(default=0)
    total_received: int = Field(default=0)
    total_sent: int = Field(default=0)
    transactions_number: int = Field(default=0, alias="n_tx", title="n_tx")
    unconfirmed_transactions_number: int = Field(default=0, alias="unconfirmed_n_tx")
    transactions_refs: List[BTCAddressTransactions] = Field(default=[], alias="txrefs", title="txrefs")
    created_at: datetime = Field(default=None)


class BTCAddressInDB(BTCAddress):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
