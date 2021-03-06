from typing import List, Optional, Literal

from fastapi import APIRouter, Query, Body, Path, responses

from core.mechanics.referrals import ReferralMechanics
from core.mechanics.user_kyc import KYCController
from core.utils import to_objectid
from database.crud import UserCRUD, UserAddressesArchiveCRUD
from schemas import (
    User,
    UserWithReferrals,
    UserKYC,
    UserUpdateNotSafe,
    UserAddressesArchive,
    USER_MODEL_INCLUDE_FIELDS,
)
from core.mechanics import UsersToExcel

__all__ = ["users_router"]

users_router = APIRouter()


@users_router.get(
    "/",
    response_model=List[User],
    response_model_include={"id", "email", "is_superuser", "is_active", "first_name", "last_name", "created_at"},
)
async def admin_users_fetch_all(
    q: Optional[str] = Query(default=None, description="query for many fields"),
    response_format: Literal["json", "excel"] = Query(default="json", description="return format", alias="format"),
):
    users = await UserCRUD.find_by_query(q, sort=[("created_at", -1)])

    if response_format == "excel":
        return responses.Response(
            UsersToExcel(users).proceed(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    return users


@users_router.get(
    "/{user_id}/",
    response_model=UserWithReferrals,
    response_model_include=USER_MODEL_INCLUDE_FIELDS.union({"_id", "email_is_active", "referrals"}),
)
async def admin_users_fetch_one(user_id: str = Path(...)):
    user = await UserCRUD.find_by_id(user_id, raise_404=True)
    user["referrals"] = await ReferralMechanics(user).fetch_referrals_top_to_bottom()
    return user


@users_router.get(
    "/{user_id}/kyc/status/",
    response_model=UserKYC,
)
async def admin_users_fetch_one_kyc(user_id: str = Path(...)):
    user = User(**await UserCRUD.find_by_id(user_id, raise_404=True))
    kyc_instance = await KYCController.init(user.id)
    return await kyc_instance.get_status()


@users_router.put(
    "/{user_id}/",
)
async def admin_users_update(user_id: str = Path(...), payload: UserUpdateNotSafe = Body(...)):
    return await UserCRUD.update_not_safe(user_id, payload)


@users_router.get("/{user_id}/archived_addresses/", response_model=List[UserAddressesArchive])
async def admin_users_fetch_archived_addresses(
    user_id: str = Path(...),
):
    return await UserAddressesArchiveCRUD.find_many({"user_id": to_objectid(user_id)}, sort=[("deleted_at", -1)])
