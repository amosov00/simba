from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.authentication import UnauthenticatedUser

__all__ = ["get_db", "get_user", "user_is_superuser"]


def get_db(request: Request):
    return request.app.mongo_db


def get_user(request: Request):
    # print(request.user.email_is_active)
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(401, "Auth is required")

    elif request.user and not request.user.email_is_active:
        raise HTTPException(401, "User is not active")

    else:
        return request.user


def user_is_staff_or_superuser(request: Request):
    user = get_user(request)

    if not user.is_staff and not user.is_superuser:
        raise HTTPException(403, "User has not enough permissions")
    else:
        return user


def user_is_superuser(request: Request):
    user = get_user(request)

    if not user.is_superuser:
        raise HTTPException(403, "User has not enough permissions")
    else:
        return user
