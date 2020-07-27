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
        user_id: Optional[str] = Query(default=None),
        email: Optional[str] = Query(default=None),
        first_name: Optional[str] = Query(default=None),
        last_name: Optional[str] = Query(default=None),
):
    q = []

    if email:
        q.append({"email": email})
    if first_name:
        q.append({"first_name": first_name})
    if last_name:
        q.append({"last_name": last_name})
    if user_id:
        try:
            q.append({"_id": ObjectId(user_id)})
        except errors.InvalidId:
            pass

    q = {"$or": q} if q else {}
    return await UserCRUD.find_many(q)


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
