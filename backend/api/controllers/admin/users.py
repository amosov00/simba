from typing import List, Optional
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query, Body, Path

from database.crud import UserCRUD, InvoiceCRUD
from schemas import (
    User,
    UserUpdateNotSafe
)

__all__ = ["users_router"]

users_router = APIRouter()


@users_router.get(
    "/",
    response_model=List[User],
    response_model_include={"id", "email", "is_superuser", "is_active", "first_name", "last_name"}
)
async def admin_users_fetch_all(
        email: Optional[str] = Query(default=None),
):
    q = []

    if email:
        q.append({"email": email})

    q = {"$and": q} if q else {}
    return await UserCRUD.find_many(q)


@users_router.get(
    "/{user_id}/",
    response_model=User,
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
