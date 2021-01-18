from http import HTTPStatus
from typing import Literal, Union
from urllib.parse import urlencode, urljoin

import httpx
from fastapi import HTTPException
from pycoin.services.blockcypher import BlockcypherProvider
from pycoin.symbols import btc, tbtx
from sentry_sdk import capture_message
from tenacity import retry, stop_after_attempt, wait_fixed

from config import IS_PRODUCTION, settings


class BlockCypherBaseAPIWrapper(BlockcypherProvider):
    def __init__(self):
        self.api_token = settings.crypto.blockcypher_token
        self.api_url = (
            "https://api.blockcypher.com/v1/btc/main" if IS_PRODUCTION else "https://api.blockcypher.com/v1/btc/test3"
        )
        self.blockcypher_wallet_name = settings.crypto.blockcypher_wallet_title
        self.netcode = "BTC" if IS_PRODUCTION else "XTN"
        self.network = btc.network if IS_PRODUCTION else tbtx.network
        super().__init__(self.api_token, self.netcode)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    async def request(
        self,
        endpoint: str,
        request_type: Literal["GET", "POST", "DELETE"] = "GET",  # Noqa
        params: dict = None,
        data: dict = None,
        with_token: bool = False,
    ) -> Union[list, dict, str, None]:

        url = self.api_url + endpoint
        params = params or {}
        params.update({"token": self.api_token}) if with_token else None

        async with httpx.AsyncClient(timeout=40.0) as client:
            if request_type == "POST":
                if params:
                    url = urljoin(url, "?" + urlencode(params))

                resp = await client.post(url, json=data)

            elif request_type == "DELETE":
                resp = await client.delete(url, params=params)

            else:
                resp = await client.get(url, params=params)

        if resp.is_error:
            capture_message(
                f"Invalid request to BlockCypher; status: {resp.status_code}; url: {url}; error {resp.text}",
                level="info",
            )
            raise HTTPException(HTTPStatus.BAD_REQUEST, resp.text)

        if resp.text:
            return resp.json()
        else:
            return resp.text
