from typing import Optional
from datetime import datetime

from pydantic import Field, validator
from passlib.context import CryptContext
from passlib import pwd

from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "pwd_context",
    "User",
    "UserLogin",
    "UserCreationSafe",
    "UserCreationNotSafe",
    "UserLoginResponse",
    "UserUpdateSafe",
    "UserUpdateNotSafe",
    "UserChangePassword",
    "UserVerifyEmail",
    "UserVerifyEmailResponse",
    "UserCreationSafeResponse"
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_email(v: str) -> str:
    return v.lower() if v else v


def validate_password(v: Optional[str], values: dict) -> str:
    if len(v) < 8:
        raise ValueError("password should be longer than 8 characters")
    if "repeat_password" in values and v != values["repeat_password"]:
        raise ValueError("passwords do not match")
    return pwd_context.hash(v)


class BaseUser(BaseModel):
    pass


class User(BaseModel):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    email: str = Field(...)
    email_is_active: Optional[bool] = Field(default=False, description="Email is validated")
    verification_code: Optional[str] = Field(default=pwd.genword(), description="Code which will send to email")
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    terms_and_condition: Optional[bool] = Field(
        default=False, description="Terms and conditions checkbox"
    )
    telegram_chat_id: Optional[int] = Field(default=None)
    telegram_id: Optional[int] = Field(default=None)
    ethereum_wallet: Optional[str] = Field(default=None)
    btc_wallet: Optional[str] = Field(default=None)
    simba_wallet: Optional[str] = Field(default=None)
    is_staff: Optional[bool] = Field(default=False, description="Staff role")
    is_superuser: Optional[bool] = Field(default=False, description="Superuser role")
    is_active: Optional[bool] = Field(default=True, description="User is active")
    btc_address: str = Field(default=None, description="Linked BTC address to user for transactions")
    created_at: Optional[datetime] = Field(default=None)

    # Is these fields in necessery ?
    # user_btc_address: str = Field(default=False, description="User BTC address")
    # user_eth_address: str = Field(default=False, description="User ETH address")

    @property
    def is_authenticated(self):
        return True

    @property
    def display_name(self):
        return self.email


class UserVerifyEmail(BaseModel):
    email: str = Field(..., example="email")
    verification_code: str = Field(..., example="verification_code")


class UserVerifyEmailResponse(BaseModel):
    msg: str = Field(..., description="Verification succeed")


class UserLogin(BaseModel):
    email: str = Field(..., example="email")
    password: str = Field(..., example="password")


class UserLoginResponse(BaseModel):
    token: str = Field(..., description="JWT token")
    user: User


class UserChangePassword(BaseModel):
    old_password: str = Field(...)
    repeat_password: str = Field(...)
    password: str = Field(...)

    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserCreationSafe(BaseModel):
    email: str = Field(...)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    repeat_password: str = Field(...)
    password: str = Field(...)

    _validate_email = validator("email", allow_reuse=True)(validate_email)
    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserCreationSafeResponse(BaseModel):
    success: bool = Field(..., description="Success or not")


class UserUpdateSafe(BaseModel):
    email: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

    _validate_email = validator("email", allow_reuse=True)(validate_email)


class UserCreationNotSafe(BaseModel):
    email: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email_is_active: Optional[bool] = Field(default=False, description="Email is validated")
    verification_code: Optional[str] = Field(default=pwd.genword(), description="Code which will send to email")
    telegram_id: Optional[int] = Field(default=None)
    telegram_chat_id: Optional[int] = Field(default=None)
    ethereum_wallet: Optional[str] = Field(default=None)
    btc_wallet: Optional[str] = Field(default=None)
    simba_wallet: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=True, description="User is active")
    is_manager: Optional[bool] = Field(default=False, description="Manager role")
    is_superuser: Optional[bool] = Field(default=False, description="Superuser role")
    repeat_password: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    _validate_email = validator("email", pre=True, allow_reuse=True)(validate_email)
    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserUpdateNotSafe(UserCreationNotSafe):
    email: Optional[str] = Field(default="")

