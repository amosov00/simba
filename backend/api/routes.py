from fastapi import APIRouter, Depends

from config import DEBUG

from api.controllers import account, debug, meta, invoice, transparency, admin
from api.dependencies import user_is_superuser

api_router = APIRouter()

# Common + user
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(meta.router, prefix="/meta", tags=["meta"])
api_router.include_router(invoice.router, prefix="/invoices", tags=["invoice"])
api_router.include_router(transparency.router, prefix="/transparency", tags=["transparency"])
api_router.include_router(
    admin.admin_router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(user_is_superuser)],
)

if DEBUG:
    api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
