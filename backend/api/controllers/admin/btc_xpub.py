from typing import List

from fastapi import APIRouter, Body, Path

from database.crud import BTCxPubCRUD
from schemas import (
    BTCxPubInDB,
    BTCxPubUpdate
)

__all__ = ["btc_xpub_router"]

btc_xpub_router = APIRouter()


@btc_xpub_router.get(
    "/",
    response_model=List[BTCxPubInDB],
    response_model_exclude={"xpub"}
)
async def admin_btc_xpub_fetch_all():
    return await BTCxPubCRUD.find_many({})


@btc_xpub_router.put(
    "/{xpub_id}/"
)
async def admin_btc_xpub_update(
        xpub_id: str = Path(...),
        payload: BTCxPubUpdate = Body(...)
):
    return await BTCxPubCRUD.update(xpub_id, payload)
