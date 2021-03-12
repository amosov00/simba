import hmac
from datetime import datetime, timedelta
from hashlib import sha1
from typing import Optional, Literal

from bson import ObjectId
from fastapi import Request

from config import settings
from core.integrations.sumsub_wrapper import SumSubWrapper
from database.crud import UserKYCCRUD
from schemas import UserKYCInDB, UserKYC, User, UserKYCDocsStatus

__all__ = ["KYCController"]


class KYCController:
    def __init__(self, user: User = None, kyc: UserKYCInDB = None):
        self.api_wrapper = SumSubWrapper()
        self.user: Optional[User] = user
        self.kyc: Optional[UserKYCInDB] = kyc

    @classmethod
    async def init(cls, user: User):
        kyc_instance = await UserKYCCRUD.find_one({"user_id": user.id})
        return cls(user, UserKYCInDB(**kyc_instance) if kyc_instance else None)

    @classmethod
    async def _generate_hashsum(cls, request: Request) -> str:
        return hmac.new(
            key=settings.person_verify.status_webhook_secret_key.encode(), msg=await request.body(), digestmod=sha1
        ).hexdigest()

    async def get_access_token(self) -> str:
        return await self.api_wrapper.get_access_token(str(self.user.id))

    @staticmethod
    def _prepare_docs_status(docs_data: dict) -> UserKYCDocsStatus:
        instance = UserKYCDocsStatus()
        if applicant_data := docs_data.get("APPLICANT_DATA"):
            instance.applicant_data = applicant_data.get("reviewResult", {}).get("reviewAnswer") == "GREEN"
        if identity_data := docs_data.get("IDENTITY"):
            instance.identity = identity_data.get("reviewResult", {}).get("reviewAnswer") == "GREEN"
        if selfie_data := docs_data.get("SELFIE"):
            instance.selfie = selfie_data.get("reviewResult", {}).get("reviewAnswer") == "GREEN"

        return instance

    @classmethod
    def _prepare_schema_data(
        cls,
        data_type: Literal["review_data", "status_data"],
        data: dict,
        user: Optional[User] = None
    ) -> UserKYC:
        if data_type == "review_data":
            result = data.get("reviewResult", {}).get("reviewAnswer") == "GREEN"

            kyc = UserKYC(
                user_id=ObjectId(request_body["externalUserId"]),  # noqa
                applicant_id=data.get("applicantId"),
                status=data.get("reviewStatus"),
                result=result,
                review_data=data,
                updated_at=datetime.now()
            )

        else:
            assert user, "user is requeired"
            docs_data = cls._prepare_docs_status(data["docs_status"])
            result = data["applicant_status"].get("reviewResult", {}).get("reviewAnswer") == "GREEN"

            kyc = UserKYC(
                user_id=user.id,
                applicant_id=data["applicant_status"].get("applicantId"),
                docs_status=docs_data,
                status=data["applicant_status"].get("reviewStatus"),
                updated_at=datetime.now(),
                status_data=data,
                result=result
            )

        return kyc

    @classmethod
    async def proceed_webhook(cls, request: Request):
        hashsum = await cls._generate_hashsum(request)

        if request.headers["x-payload-digest"] != hashsum:
            return None

        request_body = await request.json()
        payload = cls._prepare_schema_data("review_data", await request.json()).dict(exclude_unset=True)

        await UserKYCCRUD.update_or_insert(
            query={"user_id": ObjectId(request_body["externalUserId"])},
            payload=payload
        )

        return True

    async def get_status(self) -> UserKYC:
        if self.kyc:
            # Caching requests
            if self.kyc.updated_at and self.kyc.updated_at + timedelta(minutes=10) > datetime.now():
                return self.kyc

        status_data = await self.api_wrapper.get_current_status(
            applicant_id=str(self.user.id),
            service_applicant_id=self.kyc.applicant_id if self.kyc else None
        )
        payload = self._prepare_schema_data("status_data", status_data, user=self.user)

        await UserKYCCRUD.update_or_insert(
            {"user_id": self.user.id},
            payload.dict(exclude_unset=True)
        )

        return payload
