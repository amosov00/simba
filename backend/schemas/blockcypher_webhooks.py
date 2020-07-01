from typing import Literal, Optional
from datetime import datetime

from pydantic import HttpUrl

from .base import BaseModel, ObjectIdPydantic, Field

__all__ = ["BlockCypherWebhook", "BlockCypherWebhookInDB", "BlockCypherWebhookEvents", "BlockCypherWebhookCreate"]


class BlockCypherWebhookEvents:
    CONFIRMED_TX = "confirmed-tx"
    UNCONFIRMED_TX = "unconfirmed-tx"
    TX_CONFIMATION = "tx-confirmation"
    ALL = (
        CONFIRMED_TX, UNCONFIRMED_TX, TX_CONFIMATION
    )


class BlockCypherWebhook(BaseModel):
    blockcypher_id: str = Field(default=None, alias="id", title="id")
    invoice_id: ObjectIdPydantic = Field(default=None)
    token: str = None
    url: HttpUrl = None
    url_path: str = Field(default=False)
    event: str = None
    hash: Optional[str] = Field(default=None, description="Transaction / block hash")
    address: Optional[str] = Field(default=None, description="Wallet address")
    confirmations: int = None
    callback_errors: int = Field(default=0)
    created_at: datetime = Field(default=None, description="UTC")


class BlockCypherWebhookInDB(BlockCypherWebhook):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class BlockCypherWebhookCreate(BaseModel):
    blockcypher_id: str = Field(default=None, alias="id", title="id")
    invoice_id: ObjectIdPydantic = Field(...)
    event: str = Field(...)
    token: str = Field(...)
    url: HttpUrl = Field(...)
    url_path: str = Field(...)

    # Optional
    hash: Optional[str] = Field(default=None, description="Transaction / block hash")
    address: Optional[str] = Field(default=None, description="Wallet address")
    confirmations: int = Field(default=3, description="Send if confirmations more than this number")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")
