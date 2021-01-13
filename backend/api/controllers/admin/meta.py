from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Body, Path, HTTPException

from config import settings
from database.crud import MetaCRUD
from schemas import (
    MetaInDB
)

__all__ = ["meta_router"]

meta_router = APIRouter()


@meta_router.get(
    "/",
    response_model=List[MetaInDB],
)
async def admin_meta_fetch_all():
    return await MetaCRUD.find_many({})


@meta_router.get(
    "/{meta_slug}/",
    response_model=MetaInDB,
)
async def admin_meta_fetch_by_slug(
        meta_slug: str = Path(...),
):
    return await MetaCRUD.find_by_slug(meta_slug)


@meta_router.put(
    "/{meta_slug}/",
    response_model=MetaInDB
)
async def admin_meta_update(
        meta_slug: str = Path(...),
        payload: dict = Body(...)
):
    res = await MetaCRUD.find_by_slug(meta_slug)

    if res["payload"].keys() != payload.keys():
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid meta structure")

    if meta_slug == "manual_payout" and not settings.crypto.btc_multisig_wallet_address:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "multisig address not found")

    res["payload"] = payload
    await MetaCRUD.update_one({"_id": res["_id"]}, {"payload": res["payload"]})
    return res
