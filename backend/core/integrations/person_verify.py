import hashlib
import hmac
import time
from concurrent.futures.process import ProcessPoolExecutor
from urllib.parse import urljoin

import requests

from config import settings


class PersonVerifyClient:
    @classmethod
    def sign_request(cls, request: requests.Request) -> requests.PreparedRequest:
        prepared_request = request.prepare()
        now = int(time.time())
        method = request.method.upper()
        path_url = prepared_request.path_url

        body = b"" if prepared_request.body is None else prepared_request.body

        if isinstance(body, str):
            body = body.encode("utf-8")

        data_to_sign = (
            str(now).encode("utf-8")
            + method.encode("utf-8")
            + path_url.encode("utf-8")
            + body
        )

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
        params = {"userId": applicant_id, "ttlInSecs": "600"}
        headers = {"Content-Type": "application/json", "Content-Encoding": "utf-8"}

        request = cls.sign_request(
            requests.Request(
                "POST",
                urljoin(settings.person_verify.base_url, "resources/accessTokens"),
                params=params,
                headers=headers,
            )
        )

        s = requests.Session()
        response = s.send(request)

        return response.json()["token"]

    @classmethod
    async def get_access_token(cls, applicant_id: str) -> str:

        # TODO: fix this in future - replace with async aiohttp or httpx
        with ProcessPoolExecutor(max_workers=1) as pool:
            future = pool.submit(cls._get_access_token, applicant_id)

        return future.result()
