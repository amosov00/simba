from fastapi import APIRouter

from core.mechanics.crypto.bitcoin import BitcoinWrapper
from schemas import MetaSlugs, MetaCurrencyRatePayload
from database.crud import MetaCRUD

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get():
    currency_rate = await BitcoinWrapper().fetch_current_price()

    if currency_rate:
        await MetaCRUD.update_by_slug(
            slug=MetaSlugs.CURRENCY_RATE, payload=MetaCurrencyRatePayload(BTCUSD=currency_rate).dict()
        )
    return


@router.post("/")
async def debug_post():
    return {}
