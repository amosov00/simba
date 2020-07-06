from typing import Union

from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
)

from database.crud import UserCRUD
from schemas import User

__all__ = [
    "JWTAuthBackend",
]


async def auth_with_jwt(header: str) -> Union[dict, None]:
    if not header or not isinstance(header, str):
        return None

    if header:
        header = header.split(" ")

    if len(header) == 2 and header[0] == "Bearer":
        token = header[1]
        return await UserCRUD.autenticate_by_token(token)

    return None


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        user = await auth_with_jwt(
            request.headers.get("authorization") or request.headers.get("Authorization")
        )

        if user:
            user = User(**user)
            scopes = {
                "authenticated": True,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
            return AuthCredentials([key for key, val in scopes.items() if val]), user

        return None
