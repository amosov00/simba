from datetime import datetime
from typing import Union

from pydantic import Field

from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "EthereumTransaction",
    "EthereumTransactionInDB",
    "EthereumTransactionReferral",
    "SimbaContractEvents",
    "SSTContractEvents",
]


class SimbaContractEvents:
    OnIssued = "OnIssued"
    OnRedeemed = "OnRedeemed"
    Transfer = "Transfer"

    ALL = (OnIssued, OnRedeemed, Transfer)


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


class EthereumTransactionInDB(EthereumTransaction):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class EthereumTransactionReferral(EthereumTransactionInDB):
    referral_level: int = None
