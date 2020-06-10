from typing import Optional, List, Union, Tuple, Dict, Literal, Iterable
from datetime import datetime

from pydantic import Field, validator

from schemas.base import BaseModel, DecimalPydantic, ObjectIdPydantic


class EthereumTransaction(BaseModel):
    address: str = None
    args: dict = None
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
