from datetime import datetime
from enum import IntEnum
from typing import Optional, Literal, List, Union

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
    "InvoiceExtended",
    "InvoiceTransactionManual",
    "INVOICE_MODEL_EXCLUDE_FIELDS",
]

INVOICE_MODEL_EXCLUDE_FIELDS = frozenset(("sst_tx_hashes",))


class InvoiceStatus:
    CREATED = "created"
    WAITING = "waiting"  # Waiting transaction from user
    PROCESSING = "processing"  # Waiting to generate SIMBA or send BTC
    PAID = "paid"  # Paid but waiting for tx confirmation
    COMPLETED = "completed"  # success end
    CANCELLED = "cancelled"  # invoice closed
    SUSPENDED = "suspended"  # KYC and verification issues

    ALL = (CREATED, WAITING, PROCESSING, PAID, COMPLETED, CANCELLED, SUSPENDED)


class InvoiceType(IntEnum):
    BUY = 1
    SELL = 2


class Invoice(BaseModel):
    user_id: ObjectIdPydantic = Field(...)
    status: Literal[InvoiceStatus.ALL] = Field(..., description="Status title")  # noqa
    invoice_type: InvoiceType = Field(..., description="1 for buy, 2 for sell")

    # Amount
    btc_amount: Union[int, DecimalPydantic] = Field(default=0, description="Planned amount to receive / send")
    simba_amount: Union[int, DecimalPydantic] = Field(default=0, description="Planned amount to receive / send")

    btc_amount_proceeded: Union[int, DecimalPydantic] = Field(
        default=0, description="Total of BTC amount, which was received or sent"
    )
    simba_amount_proceeded: Union[int, DecimalPydantic] = Field(
        default=0, description="Total of SIMBA amount, which was received or sent"
    )

    # User wallets
    target_eth_address: Optional[str] = Field(default=None, description="Address which will be scanned")
    target_btc_address: Optional[str] = Field(default=None, description="Address which will be scanned")

    # Connected transactions
    eth_tx_hashes: List[str] = Field(default=[], description="Simba contract TX hashes")
    btc_tx_hashes: List[str] = Field(default=[])
    sst_tx_hashes: List[str] = Field(default=[], description="SST contract TX hashes")

    # Datetimes
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")
    finised_at: Optional[datetime] = Field(default=None, description="Update when completed status")

    def add_hash(self, crypto: Literal["eth", "btc", "sst"], hash_: str) -> None:
        if not hash_:
            return None
        if crypto == "eth":
            self.eth_tx_hashes = list({*self.eth_tx_hashes, hash_})
        elif crypto == "btc":
            self.btc_tx_hashes = list({*self.btc_tx_hashes, hash_})
        elif crypto == "sst":
            self.sst_tx_hashes = list({*self.sst_tx_hashes, hash_})


class InvoiceInDB(Invoice):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class InvoiceExtended(InvoiceInDB):
    eth_txs: Optional[list]
    btc_txs: Optional[list]


class InvoiceCreate(BaseModel):
    invoice_type: InvoiceType = Field(..., description="1 for buy, 2 for sell")
    btc_amount: Union[int, DecimalPydantic] = Field(default=None, description="Planned amount to receive / send", gt=0)
    simba_amount: Union[int, DecimalPydantic] = Field(
        default=None, description="Planned amount to receive / send", gt=0
    )


class InvoiceUpdate(BaseModel):
    target_eth_address: Optional[str] = Field(default=None, description="Address which will be scanned")
    target_btc_address: Optional[str] = Field(default=None, description="Address which will be scanned")

    btc_amount: Union[int, DecimalPydantic] = Field(..., description="Planned amount to receive / send", ge=0)
    simba_amount: Union[int, DecimalPydantic] = Field(..., description="Planned amount to receive / send", ge=0)

    _validate_target_btc_address = validator("target_btc_address", allow_reuse=True)(validate_btc_address)
    _validate_target_eth_address = validator("target_eth_address", allow_reuse=True)(validate_eth_address)


class InvoiceTransactionManual(BaseModel):
    btc_transaction_hash: str = None
    eth_transaction_hash: str = None
