from fastapi import APIRouter, Depends

from api.controllers import account, debug, meta, invoice, transparency, admin, ping
from api.dependencies import user_is_superuser
from config import settings

api_router = APIRouter()

# Common + user
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(meta.router, prefix="/meta", tags=["meta"])
api_router.include_router(invoice.router, prefix="/invoices", tags=["invoice"])
api_router.include_router(transparency.router, prefix="/transparency", tags=["transparency"])
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(
    admin.admin_router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(user_is_superuser)],
)

if settings.common.debug:
    api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
