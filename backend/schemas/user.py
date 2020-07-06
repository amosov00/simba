from typing import Optional, List
from datetime import datetime

from pydantic import Field, validator
from passlib.context import CryptContext
from passlib import pwd

from schemas.base import BaseModel, ObjectIdPydantic, validate_eth_address, validate_btc_address

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
    "UserCreationSafeResponse",
    "UserRecover",
    "UserRecoverLink",
    "User2faConfirm",
    "UserReferralURLResponse",
    "User2faDelete",
    "UserReferralInfo",
    "User2faURL",
    "USER_MODEL_INCLUDE_FIELDS",
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USER_MODEL_INCLUDE_FIELDS = frozenset(
    (
        "email",
        "two_factor",
        "first_name",
        "last_name",
        "signed_addresses",
        "user_btc_addresses",
        "user_eth_addresses",
        "btc_address",
        "telegram_chat_id",
        "telegram_id",
        "is_staff",
        "is_superuser",
        "is_active",
        "terms_and_condition",
        "created_at",
    )
)


def validate_email(v: str) -> str:
    return v.lower() if v else v


def validate_password(v: Optional[str], values: dict) -> str:
    if len(v) < 8:
        raise ValueError("password should be longer than 8 characters")
    if "repeat_password" in values and v != values["repeat_password"]:
        raise ValueError("passwords do not match")
    return pwd_context.hash(v)


class UserSignedAddresses(BaseModel):
    address: Optional[str] = Field(default=None)
    signature: Optional[str] = Field(default=None)


class User(BaseModel):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")

    email: str = Field(...)
    email_is_active: Optional[bool] = Field(default=False, description="Email is validated")
    verification_code: Optional[str] = Field(
        default_factory=pwd.genword, description="Code which will send to email"
    )
    recover_code: Optional[str] = Field(default=None, description="JWT token for password recover")
    secret_2fa: Optional[str] = Field(default=None, description="Code for 2fa generation")
    two_factor: Optional[bool] = Field(defaul=False, description="On/off 2fa")
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

    signed_addresses: List[UserSignedAddresses] = Field(default=[])
    user_btc_addresses: List[str] = Field(default=[])
    user_eth_addresses: List[str] = Field(default=[])

    btc_address: str = Field(default=None, description="Linked BTC address to user for transactions")

    telegram_chat_id: Optional[int] = Field(default=None)
    telegram_id: Optional[int] = Field(default=None)

    is_staff: Optional[bool] = Field(default=False, description="Staff role")
    is_superuser: Optional[bool] = Field(default=False, description="Superuser role")
    is_active: Optional[bool] = Field(default=True, description="User is active")

    terms_and_condition: Optional[bool] = Field(default=False, description="Terms and conditions checkbox")

    created_at: Optional[datetime] = Field(default=None)

    # Is these fields in necessery ?
    # ethereum_wallet: Optional[str] = Field(default=None)
    # btc_wallet: Optional[str] = Field(default=None)
    # simba_wallet: Optional[str] = Field(default=None)

    @property
    def is_authenticated(self):
        return True

    @property
    def display_name(self):
        return self.email


class UserRecover(BaseModel):
    email: str = Field(...)


class UserReferralURLResponse(BaseModel):
    URL: str = Field(...)


class UserRecoverLink(BaseModel):
    recover_code: str = Field(...)
    password: str = Field(...)
    repeat_password: str = Field(...)

    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserVerifyEmail(BaseModel):
    email: str = Field(..., example="email")
    verification_code: str = Field(..., example="verification_code")


class UserVerifyEmailResponse(BaseModel):
    msg: str = Field(..., description="Verification succeed")


class UserLogin(BaseModel):
    email: str = Field(..., example="email")
    password: str = Field(..., example="password")
    pin_code: Optional[str] = Field(default=None, example="auth pin-code")


class UserLoginResponse(BaseModel):
    token: str = Field(..., description="JWT token")


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
    referral_id: str = Field(default=None)

    _validate_email = validator("email", allow_reuse=True)(validate_email)
    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserCreationSafeResponse(BaseModel):
    success: bool = Field(..., description="Success or not")


class UserUpdateSafe(BaseModel):
    email: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

    signed_addresses: Optional[List[Optional[UserSignedAddresses]]] = Field(default=[])
    user_btc_addresses: Optional[List[str]] = Field(default=None)
    user_eth_addresses: Optional[List[str]] = Field(default=None)

    _validate_email = validator("email", allow_reuse=True)(validate_email)

    _validate_user_btc_addresses = validator("user_btc_addresses", allow_reuse=True, each_item=True)(
        validate_btc_address
    )
    _validate_user_eth_addresses = validator("user_eth_addresses", allow_reuse=True, each_item=True)(
        validate_eth_address
    )


class UserCreationNotSafe(BaseModel):
    email: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email_is_active: Optional[bool] = Field(default=False, description="Email is validated")
    verification_code: Optional[str] = Field(
        default_factory=pwd.genword, description="Code which will send to email"
    )
    referral_id: Optional[str] = Field(default=None)
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


class User2faURL(BaseModel):
    URL: str = Field(default="")


class User2faConfirm(BaseModel):
    token: str = Field(...)
    pin_code: str = Field(...)


class User2faDelete(BaseModel):
    pin_code: str = Field(...)


class UserReferralInfo(BaseModel):
    email: str = Field(...)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    referral_level: int = Field(...)
    created_at: datetime = Field(...)

    @validator("email")
    def hide_email(cls, v):
        return v.split("@")[0] + "@***.**"
