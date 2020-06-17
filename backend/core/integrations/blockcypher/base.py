from typing import Literal
from urllib.parse import urlencode, urljoin
from http import HTTPStatus

import httpx
from fastapi import HTTPException
from sentry_sdk import capture_message
from pycoin.services.blockcypher import BlockcypherProvider
from pycoin.symbols import btc, tbtx

from config import IS_PRODUCTION, BLOCKCYPHER_TOKEN, BLOCKCYPHER_WALLET_TITLE


class BlockCypherBaseAPIWrapper(BlockcypherProvider):
    def __init__(self):
        self.api_token = BLOCKCYPHER_TOKEN
        self.api_url = "https://api.blockcypher.com/v1/btc/main" \
            if IS_PRODUCTION else "https://api.blockcypher.com/v1/btc/test3"

        self.blockcypher_wallet_name = BLOCKCYPHER_WALLET_TITLE
        self.netcode = "BTC" if IS_PRODUCTION else "XTN"
        self.network = btc.network if IS_PRODUCTION else tbtx.network
        super().__init__(
            self.api_token,
            self.netcode
        )

    async def request(
            self,
            endpoint: str,
            request_type: Literal["GET", "POST", "DELETE"] = "GET",
            params: dict = None,
            data: dict = None,
            with_token: bool = False
    ) -> dict:

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
            capture_message(f"Invalid request to BlockCypher; status: {resp.status_code}; url: {url}")
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Bad request")

        return resp.json()
