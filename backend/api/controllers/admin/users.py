from typing import List, Optional

from fastapi import APIRouter, Query, Body, Path
from bson import ObjectId, errors

from database.crud import UserCRUD
from schemas import (
    User,
    UserUpdateNotSafe,
    USER_MODEL_INCLUDE_FIELDS
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
    response_model=User,
    response_model_include=USER_MODEL_INCLUDE_FIELDS.union({"_id", "email_is_active"}),
)
async def admin_users_fetch_one(user_id: str = Path(...)):
    return await UserCRUD.find_by_id(user_id)


@users_router.put(
    "/{user_id}/",
)
async def admin_users_update(
        user_id: str = Path(...),
        payload: UserUpdateNotSafe = Body(...)
):
    return await UserCRUD.update_not_safe(user_id, payload)
