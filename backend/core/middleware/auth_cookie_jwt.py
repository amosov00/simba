from typing import Union

from fastapi import Request
from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
)

from database.crud import UserCRUD
from schemas import User

__all__ = [
    "CookieJWTAuthBackend",
]


async def auth_with_cookies(cookies: dict) -> Union[dict, None]:
    # TODO make auth with cookie with httponly
    # if not header or not isinstance(header, str):
    #     return None
    #
    # if header:
    #     header = header.split(" ")
    #
    # if len(header) == 2 and header[0] == "Bearer":
    #     token = header[1]
    #     return await UserCRUD.autenticate_by_token(token)

    return None


class CookieJWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        user = await auth_with_cookies(request.cookies)

        if user:
            user = User(**user)
            scopes = {
                "authenticated": True,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
            return AuthCredentials([key for key, val in scopes.items() if val]), user

        return None
