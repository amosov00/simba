from datetime import timedelta

import sentry_sdk

from core.mechanics.crypto import BitcoinWrapper
from database.crud import MetaCRUD
from schemas import MetaSlugs, MetaCurrencyRatePayload
from workers.agents import app

__all__ = ["user_kyc_status_job"]

user_kyc_status_topic = app.topic("user_kyc_status", internal=True, retention=timedelta(minutes=10), partitions=1)


@app.agent(user_kyc_status_topic, concurrency=1)
async def user_kyc_status_job(stream):
    async for _ in stream:
        currency_rate = await BitcoinWrapper().fetch_current_price()

        if currency_rate:
            await MetaCRUD.update_by_slug(
                slug=MetaSlugs.CURRENCY_RATE, payload=MetaCurrencyRatePayload(BTCUSD=currency_rate).dict()
            )
        else:
            sentry_sdk.capture_message("Failed to fetch BTC/USD currency rate", level="error")
