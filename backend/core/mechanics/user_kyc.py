import hmac
from datetime import datetime, timedelta
from hashlib import sha1
from typing import Optional, Literal, Union

from bson import ObjectId
from fastapi import Request

from config import settings, InvoiceVerificationLimits
from core.integrations.sumsub_wrapper import SumSubWrapper
from database.crud import UserKYCCRUD, InvoiceCRUD
from schemas import (
    UserKYCInDB,
    UserKYC,
    UserKYCVerificationLimit,
    UserKYCDocsStatus,
    InvoiceStatus,
    InvoiceType,
    ObjectIdPydantic,
)

__all__ = ["KYCController"]


class KYCController:
    def __init__(self, user_id: Union[ObjectId, ObjectIdPydantic], kyc: UserKYCInDB = None):
        if not isinstance(user_id, ObjectId):
            user_id = ObjectId(user_id)

        self.api_wrapper = SumSubWrapper()
        self.user_id: ObjectId = user_id
        self.kyc_instance: Optional[UserKYCInDB] = kyc

    @classmethod
    async def init(cls, user_id: Union[str, ObjectId, ObjectIdPydantic]):
        if not isinstance(user_id, ObjectId):
            user_id = ObjectId(user_id)

        kyc_instance = await UserKYCCRUD.find_one({"user_id": user_id}) or {"user_id": user_id}
        return cls(user_id, UserKYCInDB(**kyc_instance))

    @classmethod
    async def _generate_hashsum(cls, request: Request) -> str:
        return hmac.new(
            key=settings.person_verify.status_webhook_secret_key.encode(), msg=await request.body(), digestmod=sha1
        ).hexdigest()

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

    async def get_access_token(self) -> str:
        return await self.api_wrapper.get_access_token(str(self.user_id))

    def _get_verification_limit(self) -> int:
        return InvoiceVerificationLimits.LEVEL_2 if self.kyc_instance.is_verified else InvoiceVerificationLimits.LEVEL_1

    @classmethod
    def _prepare_schema_data(
        cls, data_type: Literal["review_data", "status_data"], data: dict, user_id: Union[str, ObjectId] = None
    ) -> UserKYC:
        if not data and user_id:
            return UserKYC(**{"user_id": user_id})

        if data_type == "review_data":
            is_verified = data.get("reviewResult", {}).get("reviewAnswer") == "GREEN"

            kyc = UserKYC(
                user_id=ObjectId(request_body["externalUserId"]),  # noqa
                applicant_id=data.get("applicantId"),
                status=data.get("reviewStatus"),
                is_verified=is_verified,
                review_data=data,
                updated_at=datetime.now(),
            )

        else:
            assert user_id, "user is requeired"
            docs_data = cls._prepare_docs_status(data["docs_status"])
            is_verified = data["applicant_status"].get("reviewResult", {}).get("reviewAnswer") == "GREEN"

            kyc = UserKYC(
                user_id=user_id,  # noqa
                applicant_id=data["applicant_status"].get("applicantId"),
                docs_status=docs_data,
                status=data["applicant_status"].get("reviewStatus"),
                updated_at=datetime.now(),
                status_data=data,
                is_verified=is_verified,
            )

        return kyc

    @classmethod
    async def proceed_webhook(cls, request: Request):
        hashsum = await cls._generate_hashsum(request)

        if request.headers["x-payload-digest"] != hashsum:
            return None

        request_body = await request.json()
        payload = cls._prepare_schema_data("review_data", await request.json())

        await UserKYCCRUD.update_or_insert(
            query={"user_id": ObjectId(request_body["externalUserId"])}, payload=payload.dict(exclude_unset=True)
        )

        return True

    async def calculate_verification_limit(self, future_btc_amount: int = 0) -> UserKYCVerificationLimit:
        """Calculate user with verification / kyc limits.

        :param future_btc_amount: add to total btc to calculate previous btc + new invoice btc
        :return:
        """
        # make query
        match_stage = {
            "$match": {
                "user_id": self.user_id,
                "status": {"$in": [InvoiceStatus.COMPLETED, InvoiceStatus.PROCESSING, InvoiceStatus.SUSPENDED]},
            }
        }

        if self.kyc_instance.is_verified:
            match_stage["$match"]["finished_at"] = {"$gte": datetime.now() - timedelta(days=1)}  # noqa

        # calculate btc
        result = await InvoiceCRUD.aggregate(
            [
                match_stage,
                {
                    "$group": {
                        "_id": "$invoice_type",
                        "total_btc": {"$sum": "$btc_amount_proceeded"},
                        "total_simba": {"$sum": "$simba_amount_proceeded"},
                    }
                },
            ]
        )
        total_btc = 0
        for i in result:
            if i["_id"] == InvoiceType.BUY:
                total_btc += i["total_btc"]
            elif i["_id"] == InvoiceType.SELL:
                total_btc += i["total_simba"]

        if future_btc_amount:
            total_btc += future_btc_amount

        # calculate usd
        # btc_price = MetaCurrencyRatePayload(
        #     **(await MetaCRUD.find_by_slug(MetaSlugs.CURRENCY_RATE, raise_500=True))["payload"]
        # ).BTCUSD
        #
        # total_usd = round((total_btc * btc_price) / CryptoCurrencyRate.BTC_DECIMALS, 2)

        verification_limit = self._get_verification_limit()

        return UserKYCVerificationLimit(
            btc_used=total_btc,
            btc_remain=verification_limit - total_btc,
            btc_limit=verification_limit,
            is_allowed=verification_limit - total_btc > 0,
        )

    async def get_status(self) -> UserKYC:
        if self.kyc_instance:
            # Caching requests
            if self.kyc_instance.updated_at and self.kyc_instance.updated_at + timedelta(minutes=10) > datetime.now():
                return self.kyc_instance

        status_data = await self.api_wrapper.get_current_status(
            applicant_id=str(self.user_id),
            service_applicant_id=self.kyc_instance.applicant_id if self.kyc_instance else None,
        )

        payload = self._prepare_schema_data("status_data", status_data, user_id=self.user_id)

        await UserKYCCRUD.update_or_insert({"user_id": self.user_id}, payload.dict(exclude_unset=True))

        return payload
