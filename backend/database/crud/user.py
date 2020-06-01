from typing import Optional, Union
from datetime import datetime
from http import HTTPStatus

from fastapi.exceptions import HTTPException

from database.crud.base import BaseMongoCRUD
from core.utils.jwt import decode_jwt_token, encode_jwt_token
from core.utils import to_objectid
from schemas.user import (
    User,
    UserCreationSafe,
    UserUpdateSafe,
    pwd_context,
    UserChangePassword,
    UserUpdateNotSafe,
)

__all__ = ["UserCRUD"]

FIELDS_TO_EXCLUDE = ("repeat_password", )


class UserCRUD(BaseMongoCRUD):
    collection: str = "users"

    @classmethod
    async def find_by_id(cls, _id: str) -> Optional[dict]:
        return await super().find_one(query={"_id": to_objectid(_id)}) if _id else None

    @classmethod
    async def find_by_email(cls, email: str) -> Optional[dict]:
        return await super().find_one(query={"email": email}) if email else None

    @classmethod
    async def authenticate(cls, email: str, password: str) -> dict:
        email = email.lower()

        user = await super().find_one(query={"email": email})

        if user and pwd_context.verify(password, user["password"]):
            token = encode_jwt_token({"id": str(user["_id"])})
            return {"token": token, "user": User(**user).dict()}
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid user data")

    @classmethod
    async def autenticate_by_token(cls, token: str) -> Optional[dict]:
        token_data = decode_jwt_token(token)
        user_id = token_data.get("id") if token_data else None
        return await cls.find_by_id(user_id) if user_id else None

    @classmethod
    async def create_safe(cls, user: UserCreationSafe, **kwargs) -> dict:
        if await cls.find_by_email(user.email):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "User with this email is already exists",
            )

        inserted_id = (
            await cls.insert_one(
                payload={
                    **user.dict(exclude=set(FIELDS_TO_EXCLUDE)),
                    "created_at": datetime.now(),
                    "is_active": True,
                }
            )
        ).inserted_id

        return {
            "token": encode_jwt_token({"id": inserted_id}),
            "user": user.dict(exclude={"password", "repeat_password"}),
        }

    @classmethod
    async def update_safe(cls, user: User, payload: UserUpdateSafe) -> bool:
        if payload.email and await cls.find_by_email(payload.email):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "User with this email is already exists",
            )

        await cls.update_one(
            query={"_id": user.id}, payload=payload.dict(exclude=set(FIELDS_TO_EXCLUDE), exclude_unset=True),
        )

        return True

    @classmethod
    async def update_not_safe(cls, user_id: str, payload: UserUpdateNotSafe) -> Union[dict, User]:
        user = await cls.find_by_id(user_id)

        if not user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "User is not found")

        if not payload.dict(exclude_unset=True):
            return user

        await cls.update_one(
            query={"_id": user["_id"]},
            payload=payload.dict(exclude=set(FIELDS_TO_EXCLUDE), exclude_unset=True),
        )

        return payload.dict(
            exclude=set.union(set(FIELDS_TO_EXCLUDE), {"password", "repeat_password"}),
            exclude_unset=True,
            exclude_defaults=True,
        )

    @classmethod
    async def change_password(cls, user: User, payload: UserChangePassword) -> bool:
        old_password_obj = await cls.find_one({"_id": user.id})

        if not pwd_context.verify(payload.old_password, old_password_obj["password"]):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Old password doesn't match")

        await cls.update_one(query={"_id": user.id}, payload={"password": payload.password})

        return True
