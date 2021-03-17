from fastapi import APIRouter

from database import mongo

__all__ = ["router"]

router = APIRouter()


@router.head(
    "/",
    include_in_schema=False,
)
async def ping_head():
    return True


@router.get(
    "/",
    include_in_schema=False,
)
async def ping_get():
    return await mongo.ping()
