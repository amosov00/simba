from typing import Literal

from pydantic import HttpUrl

from .base import BaseModel, ObjectIdPydantic, Field

__all__ = ["BlockCypherWebhook", "BlockCypherWebhookInDB", "BlockCypherWebhookEvents"]


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


class BlockCypherWebhookInDB(BlockCypherWebhook):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
