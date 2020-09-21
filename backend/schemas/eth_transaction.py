from datetime import datetime
from typing import Union

from schemas.base import BaseModel, ObjectIdPydantic, Field

__all__ = [
    "EthereumTransaction",
    "EthereumTransactionInDB",
    "SimbaContractEvents",
    "SSTContractEvents",
]


class SimbaContractEvents:
    OnIssued = "OnIssued"
    OnRedeemed = "OnRedeemed"
    Transfer = "Transfer"
    BlacklistedAdded = "BlacklistedAdded"
    BlacklistedRemoved = "BlacklistedRemoved"

    ALL = (OnIssued, OnRedeemed, Transfer, BlacklistedAdded, BlacklistedRemoved)


class SSTContractEvents:
    OnFreezed = "OnFreezed"
    Transfer = "Transfer"
    ALL = (OnFreezed, Transfer)


class EthereumTransaction(BaseModel):
    invoice_id: ObjectIdPydantic = None
    user_id: ObjectIdPydantic = None
    bitcoins_sended: bool = False
    address: str = None
    args: dict = None
    confirmations: int = None
    blockHash: Union[str] = None
    blockNumber: int = None
    logIndex: int = None
    transactionHash: Union[str] = None
    transactionIndex: int = None
    event: str = None
    contract: str = None
    fetched_at: datetime = None
    skip: bool = Field(default=False, description="Skip in search cause transaction is irrelevant in processing")


class EthereumTransactionInDB(EthereumTransaction):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
