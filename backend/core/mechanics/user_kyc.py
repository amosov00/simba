import hmac
from datetime import datetime, timedelta
from hashlib import sha1

from bson import ObjectId
from fastapi import Request

from config import settings
from core.integrations.sumsub_wrapper import SumSubWrapper
from database.crud import UserCRUD, UserKYCCRUD
from schemas import UserKYC, User

__all__ = ["KYCController"]


class KYCController:
    def __init__(self):
        self.api_wrapper = SumSubWrapper()

    @classmethod
    async def _generate_hashsum(cls, request: Request) -> str:
        return hmac.new(
            key=settings.person_verify.status_webhook_secret_key.encode(), msg=await request.body(), digestmod=sha1
        ).hexdigest()

    async def get_access_token(self, user: User) -> str:
        return await self.api_wrapper.get_access_token(str(user.id))

    async def _prepare_schema_data(self, data: dict) -> UserKYC:
        pass

    async def proceed_webhook(self, request: Request):
        hashsum = await self._generate_hashsum(request)

        if request.headers["x-payload-digest"] != hashsum:
            return None

        request_body = await request.json()
        await UserKYCCRUD.update_or_insert(
            {"user_id": ObjectId(request_body["externalUserId"])},
            UserKYC(
                user_id=ObjectId(request_body["externalUserId"]),  # noqa
                result=request_body["reviewResult"].get("reviewAnswer"),
                status=request_body["reviewStatus"],
                review_data=request_body,
            ).dict(exclude_unset=True),
        )

        return True

    async def get_current_status(self, user: User):
        kyc_current_status = user.kyc_current_status

        if not kyc_current_status or (kyc_current_status and datetime.now() >= kyc_current_status.get("_expire_at")):
            kyc_current_status = await self.api_wrapper.get_current_status(
                applicant_id=str(user.id),
                service_applicant_id=kyc_current_status.get("service_applicant_id_cache")
                if kyc_current_status
                else None,
            )

            expire_at = datetime.now() + timedelta(minutes=5)  # default cache expire time

            kyc_current_status["_expire_at"] = expire_at

            await UserCRUD.update_one({"_id": user.id}, {"kyc_current_status": kyc_current_status})

        return kyc_current_status
