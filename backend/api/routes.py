from fastapi import APIRouter

from config import DEBUG

from api.controllers import account, debug, crypto

api_router = APIRouter()

api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(crypto.router, prefix="/crypto", tags=["crypto"])


if DEBUG:
    api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
