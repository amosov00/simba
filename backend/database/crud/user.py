import asyncio
from typing import Optional, Union
from passlib import pwd
from datetime import datetime, timedelta
from http import HTTPStatus

import pyotp
from fastapi.exceptions import HTTPException

from database.crud.base import BaseMongoCRUD
from database.crud.referral import ReferralCRUD
from core.utils.jwt import decode_jwt_token, encode_jwt_token
from core.utils.email import Email, MailGunEmail
from core.utils import to_objectid
from .base import ObjectId
from schemas.user import (
    User,
    UserCreationSafe,
    UserCreationNotSafe,
    UserUpdateSafe,
    pwd_context,
    UserChangePassword,
    UserUpdateNotSafe,
    UserRecover,
    UserRecoverLink,
    User2faConfirm,
    User2faDelete,
    UserReferralInfo,
)

__all__ = ["UserCRUD"]

FIELDS_TO_EXCLUDE = ("repeat_password", "recover_code", "secret_2fa", "referral_id")


class UserCRUD(BaseMongoCRUD):
    collection: str = "users"

    @classmethod
    async def find_by_email(cls, email: str) -> Optional[dict]:
        return await super().find_one(query={"email": email}) if email else None

    @classmethod
    async def check_2fa(cls, user_id: ObjectId, pin_code: str) -> bool:
        user = await cls.find_by_id(user_id)
        totp = pyotp.TOTP(user["secret_2fa"])
        current_pin_code = totp.now()
        return pin_code == current_pin_code

    @classmethod
    async def authenticate(cls, email: str, password: str, pin_code: Optional[str] = None) -> dict:
        email = email.lower()

        user = await cls.find_one(query={"email": email})

        if not user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "User with such email not found")

        if not user.get("email_is_active"):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Activate your account")

        if pwd_context.verify(password, user["password"]):

            if user.get("two_factor") is True and not await cls.check_2fa(user["_id"], pin_code):
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect 2FA pin code")

            token = encode_jwt_token({"id": str(user["_id"])})
            return {"token": token}
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid user data")

    @classmethod
    async def verify_email(cls, email: str, verification_code: str) -> dict:
        email = email.lower()

        user = await super().find_one(query={"email": email})

        if not user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "No such user with that email")
        if user["email_is_active"]:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "User already verified")

        if user["verification_code"] == verification_code:
            user["email_is_active"] = True
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong verification code")

        user["verification_code"] = None

        await cls.update_one(
            query={"_id": user["_id"]},
            payload={
                "verification_code": user["verification_code"],
                "email_is_active": user["email_is_active"],
            },
        )

        keys = {"password", "repeat_password", "verification_code"}
        return {
            "token": encode_jwt_token({"id": user["_id"]}),
            "user": {x: user[x] for x in user if x not in keys},
        }

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

        referral_user = await cls.find_by_id(user.referral_id)

        if not referral_user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Referral link invalid")

        verification_code = pwd.genword()

        inserted_id = (
            await cls.insert_one(
                payload={
                    **user.dict(exclude=set(FIELDS_TO_EXCLUDE)),
                    "created_at": datetime.now(),
                    "is_active": True,
                    "email_is_active": False,
                    "verification_code": verification_code,
                }
            )
        ).inserted_id

        asyncio.create_task(MailGunEmail().send_verification_code(user.email, verification_code))

        await ReferralCRUD.add_referral(inserted_id, referral_user["_id"])

        return {"success": True}

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
    async def create_not_safe(cls, user: UserCreationNotSafe, **kwargs) -> Optional[dict]:
        if await cls.find_by_email(user.email):
            return None

        await super().insert_one(
            payload={**user.dict(exclude=set(FIELDS_TO_EXCLUDE)), "created_at": datetime.now(), **kwargs}
        )

        return {"success": True}

    @classmethod
    async def update_not_safe(cls, user_id: str, payload: UserUpdateNotSafe):
        user = await cls.find_by_id(user_id)

        if not user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "User is not found")

        if not payload.dict(exclude_unset=True):
            return user

        payload = payload.dict(
            exclude=set.union(set(FIELDS_TO_EXCLUDE), {"password", "repeat_password"}),
            exclude_unset=True,
            exclude_defaults=True,
        )

        return bool((await cls.update_one(
            query={"_id": user["_id"]},
            payload=payload
        )).modified_count)

    @classmethod
    async def change_password(cls, user: User, payload: UserChangePassword) -> bool:
        old_password_obj = await cls.find_one({"_id": user.id})

        if not pwd_context.verify(payload.old_password, old_password_obj["password"]):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Old password doesn't match")

        await cls.update_one(query={"_id": user.id}, payload={"password": payload.password})

        return True

    @classmethod
    async def recover_send(cls, payload: UserRecover):
        user = await cls.find_by_email(payload.email)

        if not user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "No such user")

        recover_code = encode_jwt_token({"_id": user["_id"]}, timedelta(hours=3))

        await cls.update_one({"_id": user["_id"]}, {"recover_code": recover_code})
        asyncio.create_task(MailGunEmail().send_recover_code(user["email"], recover_code))
        return True

    @classmethod
    async def recover(cls, payload: UserRecoverLink):
        data = decode_jwt_token(payload.recover_code)

        if data is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect code")

        user_id = data["_id"]

        user = await cls.find_one({"_id": ObjectId(user_id)})

        if "recover_code" not in user or user["recover_code"] != payload.recover_code:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect code")

        await cls.update_one(
            query={"_id": user["_id"]}, payload={"password": payload.password, "recover_code": None}
        )

        return True

    @classmethod
    async def create_2fa(cls, user: User):
        secret_2fa = pyotp.random_base32()
        target_url = pyotp.totp.TOTP(secret_2fa).provisioning_uri(user.email, issuer_name="Simba")
        return {"URL": target_url}

    @classmethod
    async def confirm_2fa(cls, user: User, payload: User2faConfirm):
        totp = pyotp.TOTP(payload.token)
        current_pin_code = totp.now()
        if current_pin_code != payload.pin_code:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect pin-code")
        await cls.update_one(query={"_id": user.id}, payload={"secret_2fa": payload.token, "two_factor": True})
        return True

    @classmethod
    async def delete_2fa(cls, user: User, payload: User2faDelete):
        current_pin_code = pyotp.TOTP(user.secret_2fa).now()
        if current_pin_code != payload.pin_code:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect pin-code")
        await cls.update_one(query={"_id": user.id}, payload={"secret_2fa": None, "two_factor": False})
        return True
