from fastapi import APIRouter

from database import mongo

__all__ = ["router"]

router = APIRouter()


@router.get(
    "/",
    include_in_schema=False,
)
async def ping():
    return await mongo.ping()
