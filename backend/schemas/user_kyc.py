from datetime import datetime
from typing import Optional

from schemas.base import BaseModel, ObjectIdPydantic, Field

__all__ = ["UserKYC", "UserKYCDocsStatus", "UserKYCInDB", "UserKYCAccessTokenResponse", "UserKYCVerificationLimit"]


class UserKYCDocsStatus(BaseModel):
    applicant_data: bool = Field(default=False)
    identity: bool = Field(default=False)
    selfie: bool = Field(default=False)


class UserKYC(BaseModel):
    user_id: ObjectIdPydantic = Field(...)
    applicant_id: Optional[str] = Field(default=None)  # applicantId
    is_verified: bool = Field(default=False)  # reviewResult.reviewAnswer
    status: Optional[str] = Field(default=None)  # reviewStatus

    docs_status: UserKYCDocsStatus = Field(default_factory=UserKYCDocsStatus)

    review_data: dict = Field(default={})
    status_data: dict = Field(default={})

    updated_at: datetime = Field(default=None)


class UserKYCResponse(UserKYC):
    allowed_usd: Optional[int] = Field(default=2000)


class UserKYCInDB(UserKYC):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class UserKYCVerificationLimit(BaseModel):
    btc_used: float = Field(default=0.0)
    btc_remain: float = Field(default=0.0)
    btc_limit: float = Field(default=0.0)
    is_allowed: bool = Field(default=False)


class UserKYCAccessTokenResponse(BaseModel):
    token: str = Field(...)
