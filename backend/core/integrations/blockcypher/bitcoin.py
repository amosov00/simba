from typing import Literal, Optional
from urllib.parse import urlencode, urljoin
from http import HTTPStatus

import httpx
from fastapi import HTTPException
from sentry_sdk import capture_message
from pycoin.services.blockcypher import BlockcypherProvider
from pycoin.symbols import btc, tbtx
from pycoin.coins.Tx import Tx

from config import IS_PRODUCTION, BLOCKCYPHER_TOKEN, BLOCKCYPHER_WALLET_TITLE
from schemas import BTCAddress, BTCTransaction


class BlockCypherAPIWrapper(BlockcypherProvider):
    api_token = BLOCKCYPHER_TOKEN
    api_url = "https://api.blockcypher.com/v1/btc/main" \
        if IS_PRODUCTION else "https://api.blockcypher.com/v1/btc/test3"

    blockcypher_wallet_name = BLOCKCYPHER_WALLET_TITLE

    def __init__(self):
        self.netcode = "BTC" if IS_PRODUCTION else "XTN"
        self.network = btc.network if IS_PRODUCTION else tbtx.network
        super().__init__(
            self.api_token,
            self.netcode
        )

    async def request(
            self,
            endpoint: str,
            request_type: Literal["GET", "POST"] = "get",
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

            else:
                resp = await client.get(url, params=params)

        if resp.is_error:
            capture_message(f"Invalid request to BlockCypher; status: {resp.status_code}; url: {url}")
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Bad request")

        return resp.json()

    async def create_wallet_address(self, quantity: int = 1) -> dict:
        endpoint = f"/wallets/hd/{self.blockcypher_wallet_name}/addresses/derive"
        return await self.request(endpoint, "POST", {"count": quantity}, with_token=True)

    async def fetch_address_info(self, address_hash: str) -> Optional[BTCAddress]:
        endpoint = f"/addrs/{address_hash}/"
        res = await self.request(endpoint)
        return BTCAddress(**res) if res else None

    async def fetch_transaction_info(self, transaction_hash: str) -> Optional[BTCTransaction]:
        endpoint = f"/txs/{transaction_hash}/"
        res = await self.request(endpoint)
        return BTCTransaction(**res) if res else None

    async def create_transaction(self, data: dict) -> dict:
        endpoint = f"/txs/new/"
        res = await self.request(endpoint, request_type="POST", data=data)
        return res

    async def send_transaction(self, data: dict):
        endpoint = f"/txs/send/"
        res = await self.request(endpoint, request_type="POST", data=data, with_token=True)
        return res

    async def push_raw_tx(self, tx: Tx):
        endpoint = f"/txs/push/"
        data = {"tx": tx.as_hex()}
        res = await self.request(endpoint, request_type="POST", data=data, with_token=True)
        return res

    async def get_payables(self, address: str):
        return self.get_payables(address)
