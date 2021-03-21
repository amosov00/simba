import hashlib
import hmac
import time
from http import HTTPStatus
from typing import Optional
from urllib.parse import urljoin

import requests

from config import settings


class SumSubWrapper:
    @classmethod
    def sign_request(cls, request: requests.Request) -> requests.PreparedRequest:
        prepared_request = request.prepare()
        now = int(time.time())
        method = request.method.upper()
        path_url = prepared_request.path_url

        body = b"" if prepared_request.body is None else prepared_request.body

        if isinstance(body, str):
            body = body.encode("utf-8")

        data_to_sign = str(now).encode("utf-8") + method.encode("utf-8") + path_url.encode("utf-8") + body

        signature = hmac.new(
            settings.person_verify.secret_key.encode("utf-8"),
            data_to_sign,
            digestmod=hashlib.sha256,
        )

        prepared_request.headers["X-App-Token"] = settings.person_verify.app_token
        prepared_request.headers["X-App-Access-Ts"] = str(now)
        prepared_request.headers["X-App-Access-Sig"] = signature.hexdigest()

        return prepared_request

    @classmethod
    def _get_access_token(cls, applicant_id: str) -> str:
        request = cls.sign_request(
            requests.Request(
                "POST",
                url=urljoin(settings.person_verify.base_url, "resources/accessTokens"),
                params={"userId": applicant_id, "ttlInSecs": "600"},
                headers={"Content-Type": "application/json", "Content-Encoding": "utf-8"},
            )
        )

        s = requests.Session()
        response = s.send(request)

        return response.json()["token"]

    @classmethod
    def _get_service_applicant_id(cls, applicant_id: str) -> Optional[str]:
        params = {"userId": applicant_id, "ttlInSecs": "600"}
        headers = {"Content-Type": "application/json", "Content-Encoding": "utf-8"}

        request = cls.sign_request(
            requests.Request(
                "GET",
                urljoin(settings.person_verify.base_url, f"/resources/applicants/-;externalUserId={applicant_id}/one"),
                params=params,
                headers=headers,
            )
        )

        s = requests.Session()
        response = s.send(request)

        if response.status_code != HTTPStatus.OK:
            return None

        return response.json()["id"]

    @classmethod
    def _get_current_status(cls, applicant_id: Optional[str]) -> Optional[dict]:
        if not applicant_id:
            return None

        params = {"userId": applicant_id, "ttlInSecs": "600"}
        headers = {"Content-Type": "application/json", "Content-Encoding": "utf-8"}

        status = {}

        request = cls.sign_request(
            requests.Request(
                "GET",
                urljoin(settings.person_verify.base_url, f"resources/applicants/{applicant_id}/status"),
                params=params,
                headers=headers,
            )
        )

        s = requests.Session()
        response = s.send(request)

        status["applicant_status"] = response.json()

        request = cls.sign_request(
            requests.Request(
                "GET",
                urljoin(settings.person_verify.base_url, f"resources/applicants/{applicant_id}/requiredIdDocsStatus"),
                params=params,
                headers=headers,
            )
        )

        s = requests.Session()
        response = s.send(request)

        status["docs_status"] = response.json()

        return status

    @classmethod
    async def get_access_token(cls, applicant_id: str) -> str:
        return cls._get_access_token(applicant_id=applicant_id)

    @classmethod
    async def get_current_status(cls, applicant_id: str, service_applicant_id: Optional["str"] = None) -> Optional[dict]:
        if not service_applicant_id:
            service_applicant_id = cls._get_service_applicant_id(applicant_id)

        return cls._get_current_status(service_applicant_id)
