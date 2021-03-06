from datetime import datetime

from .base import BaseModel, ObjectIdPydantic, Field

__all__ = ["Meta", "MetaInDB", "MetaSlugs", "MetaManualPayoutPayload", "MetaCurrencyRatePayload"]


class MetaSlugs:
    MANUAL_PAYOUT = "manual_payout"
    EMAIL_TO_SUPPORT_TIME = "email_to_support_time"
    BLACKLISTED_BALANCE = "blacklisted_balance"
    CURRENCY_RATE = "currency_rate"
    SIMBA_META = "simba_meta"
    EMAIL_SUPPORT_HOT_WALLET_BALANCE_LACK = "email_support_hot_wallet_balance_lack"
    EMAIL_SUPPORT_INVOICE_STUCK = "email_support_invoice_stuck"


class MetaManualPayoutPayload(BaseModel):
    is_active: bool = Field(default=False)


class MetaCurrencyRatePayload(BaseModel):
    BTCUSD: float = Field(default=None)


class Meta(BaseModel):
    slug: str = Field(...)
    payload: dict = Field(...)
    updated_at: datetime = Field(default_factory=datetime.now)


class MetaInDB(Meta):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
