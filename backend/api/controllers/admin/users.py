from typing import List, Optional

from fastapi import APIRouter, Query, Body, Path

from core.utils import to_objectid
from database.crud import UserCRUD, UserAddressesArchiveCRUD
from core.mechanics.referrals import ReferralMechanics
from schemas import (
    User,
    UserWithReferrals,
    UserUpdateNotSafe,
    UserAddressesArchive,
    USER_MODEL_INCLUDE_FIELDS,
)

__all__ = ["users_router"]

users_router = APIRouter()


@users_router.get(
    "/",
    response_model=List[User],
    response_model_include={"id", "email", "is_superuser", "is_active", "first_name", "last_name"}
)
async def admin_users_fetch_all(
        q: Optional[str] = Query(default=None, description="query for many fields"),
):
    return await UserCRUD.find_by_query(q)


@users_router.get(
    "/{user_id}/",
    response_model=UserWithReferrals,
    response_model_include=USER_MODEL_INCLUDE_FIELDS.union({"_id", "email_is_active", "referrals"}),
)
async def admin_users_fetch_one(user_id: str = Path(...)):
    user = await UserCRUD.find_by_id(user_id, raise_404=True)
    user["referrals"] = await ReferralMechanics(user).fetch_referrals_top_to_bottom()
    return user


@users_router.put(
    "/{user_id}/",
)
async def admin_users_update(
        user_id: str = Path(...),
        payload: UserUpdateNotSafe = Body(...)
):
    return await UserCRUD.update_not_safe(user_id, payload)


@users_router.get(
    "/{user_id}/archived_addresses/",
    response_model=List[UserAddressesArchive]
)
async def admin_users_fetch_archived_addresses(
        user_id: str = Path(...),
):
    return await UserAddressesArchiveCRUD.find_many({"user_id": to_objectid(user_id)}, sort=[("deleted_at", -1)])
