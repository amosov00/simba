from fastapi import APIRouter, Depends

from api.dependencies import user_is_superuser

from .users import *
from .invoice import *
from .btc_xpub import *
from .meta import *

__all__ = ["admin_router"]

admin_router = APIRouter()

# Admin
admin_router.include_router(
    users_router,
    prefix="/users",
    dependencies=[Depends(user_is_superuser)]
)
admin_router.include_router(
    invoices_router,
    prefix="/invoices",
    dependencies=[Depends(user_is_superuser)]
)
admin_router.include_router(
    btc_xpub_router,
    prefix="/btc-xpub",
    dependencies=[Depends(user_is_superuser)]
)
admin_router.include_router(
    meta_router,
    prefix="/meta",
    dependencies=[Depends(user_is_superuser)]
)
