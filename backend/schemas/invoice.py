from typing import Optional, Literal, List, Union
from datetime import datetime
from enum import IntEnum

from pydantic import Field, validator

from schemas.base import BaseModel, ObjectIdPydantic, DecimalPydantic, validate_btc_address, validate_eth_address

__all__ = ['InvoiceStatus', 'InvoiceType', 'Invoice', 'InvoiceUpdate', 'InvoiceCreate', 'InvoiceInDB']


class InvoiceStatus:
    CREATED = 'created'
    WAITING = 'waiting'  # Waiting transaction from user
    PROCESSING = 'processing'  # Waiting to generate SIMBA or send BTC
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    ALL = (
        CREATED, WAITING, PROCESSING, COMPLETED, CREATED
    )


class InvoiceType(IntEnum):
    BUY = 1
    SELL = 2


class Invoice(BaseModel):
    user_id: ObjectIdPydantic = Field(..., alias="_id", title="_id")
    status: Literal[InvoiceStatus.ALL] = Field(..., description="Status title")  # noqa
    invoice_type: InvoiceType = Field(..., description="1 for buy, 2 for sell")

    # Amount
    btc_amount: Union[int, DecimalPydantic] = Field(default=0)
    simba_amount: Union[int, DecimalPydantic] = Field(default=0)
    fee: Union[int, str] = Field(default=0)

    # TODO Сколько крипты было перечислено. Некорректное использование полей, найти вариант лучше
    btc_amount_deposited: Union[int, DecimalPydantic] = Field(default=0)
    simba_amount_deposited: Union[int, DecimalPydantic] = Field(default=0)

    # User wallets
    target_eth_address: str = Field(default="", description="Address which will be scanned")
    target_btc_address: str = Field(default="", description="Address which will be scanned")

    # TODO Maybe it will be not necessery
    # user_eth_address: str = Field(default="", description="")
    # user_btc_address: str = Field(default="", description="")

    # Connected transactions
    eth_tx: List[ObjectIdPydantic] = Field(default=[])
    btc_tx: List[ObjectIdPydantic] = Field(default=[])

    # Datetimes
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")
    finised_at: Optional[datetime] = Field(default="")

    # Validate transaction before processing
    validation_md5_hash: str = Field(default="")

    # Validators. TODO Нужно ли использовать валидаторы здесь? Это сильно замедлит валидацию большого кол-ва
    # данные
    # _validate_user_btc_address = validator("user_btc_address", allow_reuse=True)(validate_btc_address)
    # _validate_user_eth_address = validator("user_eth_address", allow_reuse=True)(validate_eth_address)
    # _validate_target_btc_address = validator("target_btc_address", allow_reuse=True)(validate_btc_address)
    # _validate_target_eth_address = validator("target_eth_address", allow_reuse=True)(validate_eth_address)


class InvoiceInDB(Invoice):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class InvoiceCreate(Invoice):
    status: Literal[InvoiceStatus.ALL] = InvoiceStatus.CREATED  # noqa


class InvoiceUpdate(BaseModel):
    target_eth_address: str = Field(default="")
    target_btc_address: str = Field(default="")
    btc_amount: Union[int, DecimalPydantic] = Field(default=0)
    simba_amount: Union[int, DecimalPydantic] = Field(default=0)

    _validate_target_btc_address = validator("target_btc_address", allow_reuse=True)(validate_btc_address)
    _validate_target_eth_address = validator("target_eth_address", allow_reuse=True)(validate_eth_address)

    # TODO Maybe it will be not necessery
    # user_eth_address: str = Field(default="")
    # user_btc_address: str = Field(default="")
    # _validate_user_btc_address = validator("user_btc_address", allow_reuse=True)(validate_btc_address)
    # _validate_user_eth_address = validator("user_eth_address", allow_reuse=True)(validate_eth_address)
