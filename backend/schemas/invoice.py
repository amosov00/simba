from typing import Optional, Literal, List, Union
from datetime import datetime
from enum import IntEnum

from pydantic import Field, validator

from schemas.base import (
    BaseModel,
    ObjectIdPydantic,
    DecimalPydantic,
    validate_btc_address,
    validate_eth_address,
)

__all__ = [
    "InvoiceStatus",
    "InvoiceType",
    "Invoice",
    "InvoiceUpdate",
    "InvoiceCreate",
    "InvoiceInDB",
    "InvoiceTransactionManual",
]


class InvoiceStatus:
    CREATED = "created"
    WAITING = "waiting"  # Waiting transaction from user
    PROCESSING = "processing"  # Waiting to generate SIMBA or send BTC
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    ALL = (CREATED, WAITING, PROCESSING, COMPLETED, CANCELLED)


class InvoiceType(IntEnum):
    BUY = 1
    SELL = 2


class Invoice(BaseModel):
    user_id: ObjectIdPydantic = Field(...)
    status: Literal[InvoiceStatus.ALL] = Field(..., description="Status title")  # noqa
    invoice_type: InvoiceType = Field(..., description="1 for buy, 2 for sell")

    # Amount
    btc_amount: Union[int, DecimalPydantic] = Field(default=None, description="Planned amount to receive / send")
    simba_amount: Union[int, DecimalPydantic] = Field(default=None, description="Planned amount to receive / send")

    btc_amount_proceeded: Union[int, DecimalPydantic] = Field(
        default=0, description="Total of BTC amount, which was received or sent"
    )
    simba_amount_proceeded: Union[int, DecimalPydantic] = Field(
        default=0, description="Total of SIMBA amount, which was received or sent"
    )

    # User wallets
    target_eth_address: str = Field(default=None, description="Address which will be scanned")
    target_btc_address: str = Field(default=None, description="Address which will be scanned")

    # Connected transactions
    eth_tx_ids: List[ObjectIdPydantic] = Field(default=[])
    btc_tx_ids: List[ObjectIdPydantic] = Field(default=[])

    # Datetimes
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")
    finised_at: Optional[datetime] = Field(default=None, description="Update when completed status")

    # Validate transaction before processing
    validation_md5_hash: str = Field(default="")


class InvoiceInDB(Invoice):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class InvoiceCreate(BaseModel):
    invoice_type: InvoiceType = Field(..., description="1 for buy, 2 for sell")  # noqa


class InvoiceUpdate(BaseModel):
    target_eth_address: str = Field(default=None, description="Address which will be scanned")
    target_btc_address: str = Field(default=None, description="Address which will be scanned")

    btc_amount: Union[int, DecimalPydantic] = Field(default=None, description="Planned amount to receive / send")
    simba_amount: Union[int, DecimalPydantic] = Field(default=None, description="Planned amount to receive / send")

    _validate_target_btc_address = validator("target_btc_address", allow_reuse=True)(validate_btc_address)
    _validate_target_eth_address = validator("target_eth_address", allow_reuse=True)(validate_eth_address)


class InvoiceTransactionManual(BaseModel):
    eth_transaction_hash: str = None
    btc_transaction_hash: str = None
