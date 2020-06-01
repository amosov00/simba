from fastapi import APIRouter

from config import DEBUG

from api.controllers import account, debug

api_router = APIRouter()

api_router.include_router(account.router, prefix="/account", tags=["account"])


if DEBUG:
    api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
