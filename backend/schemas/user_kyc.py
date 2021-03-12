from typing import Optional
from datetime import datetime

from schemas.base import BaseModel, ObjectIdPydantic, Field

__all__ = ["UserKYC", "UserKYCDocsStatus", "UserKYCInDB", "UserKYCAccessTokenResponse"]


class UserKYCDocsStatus(BaseModel):
    applicant_data: bool = Field(default=False)
    identity: bool = Field(default=False)
    selfie: bool = Field(default=False)


class UserKYC(BaseModel):
    user_id: ObjectIdPydantic = Field(...)
    applicant_id: Optional[str] = Field(default=None)  # applicantId
    result: bool = Field(default=False)  # reviewResult.reviewAnswer
    status: Optional[str] = Field(default=None)  # reviewStatus

    docs_status: UserKYCDocsStatus = Field(default_factory=UserKYCDocsStatus)

    review_data: dict = Field(default={})
    status_data: dict = Field(default={})

    updated_at: datetime = Field(default=None)


class UserKYCInDB(UserKYC):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class UserKYCAccessTokenResponse(BaseModel):
    token: str = Field(...)
