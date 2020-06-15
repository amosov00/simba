from typing import Optional
from datetime import datetime

from pydantic import Field, validator

from schemas.base import BaseModel, ObjectIdPydantic

__all__ = ['Invoice']


class Invoice(BaseModel):
    type: bool = Field(...)  # (1 - sell)  (0 - buy)
    user_id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    created_at: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default=None)
    buy_user_eth_address: Optional[str] = Field(default=None)
    buy_btc_address: Optional[str] = Field(default=None)
    buy_amount_btc: Optional[float] = Field(default=None)
    buy_receive_simba: Optional[float] = Field(default=None)
    sell_btc_address: Optional[str] = Field(default=None)
    sell_amount_simba: Optional[float] = Field(default=None)
    sell_receive_btc: Optional[float] = Field(default=None)


class CreateInvoiceSell(BaseModel):
    type: bool = Field(default=True)
    user_id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    created_at: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default='created')
    sell_btc_address: Optional[str] = Field(default=None)
    sell_amount_simba: Optional[float] = Field(default=None)
    sell_receive_btc: Optional[float] = Field(default=None)


class CreateInvoiceBuy(BaseModel):
    type: bool = Field(default=False)
    user_id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    created_at: Optional[datetime] = Field(default='created')
    status: Optional[str] = Field(default=None)
    buy_user_eth_address: Optional[str] = Field(default=None)
    buy_btc_address: Optional[str] = Field(default=None)
    buy_amount_btc: Optional[float] = Field(default=None)
    buy_receive_simba: Optional[float] = Field(default=None)
