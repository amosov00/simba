from typing import Literal, Optional

from pydantic import HttpUrl

from .base import BaseModel, ObjectIdPydantic, Field

__all__ = ["BlockCypherWebhook", "BlockCypherWebhookInDB", "BlockCypherWebhookEvents", "BlockCypherWebhookCreate"]


class BlockCypherWebhookEvents:
    UNCONFIRMED_TX = "unconfirmed-tx"
    TX_CONFIMATION = "tx-confirmation"

    ALL = (
        UNCONFIRMED_TX, TX_CONFIMATION
    )


class BlockCypherWebhook(BaseModel):
    id: str = Field(...)
    event: str = Field(...)
    address: str = Field(...)
    token: str = Field(...)
    url: HttpUrl = Field(...)
    callback_errors: int = Field(default=0)


class BlockCypherWebhookCreate(BaseModel):
    id: str = Field(...)
    invoice_id: ObjectIdPydantic = Field(...)
    event: str = Field(...)
    token: str = Field(...)
    url: HttpUrl = Field(...)

    # Optional
    hash: Optional[str] = Field(default=None, description="Transaction / block hash")
    address: Optional[str] = Field(default=None, description="Wallet address")
    confirmations: int = Field(default=3, description="Send if confirmations more than this number")
    # wallet_name: Optional[str] = None


class BlockCypherWebhookInDB(BlockCypherWebhook):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
