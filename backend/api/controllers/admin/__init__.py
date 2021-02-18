from fastapi import APIRouter

from .background_jobs import router as background_jobs_router
from .btc_xpub import *
from .invoice import *
from .meta import *
from .users import *

__all__ = ["admin_router"]

admin_router = APIRouter()

admin_router.include_router(
    users_router,
    prefix="/users",
)
admin_router.include_router(
    invoices_router,
    prefix="/invoices",
)
admin_router.include_router(
    btc_xpub_router,
    prefix="/btc-xpub",
)
admin_router.include_router(
    meta_router,
    prefix="/meta",
)
admin_router.include_router(
    background_jobs_router,
    prefix="/background-jobs",
)
