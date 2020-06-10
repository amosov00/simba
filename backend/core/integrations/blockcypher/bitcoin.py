from typing import Literal, Optional
from urllib.parse import urlencode, urljoin

import httpx

from config import IS_PRODUCTION, BLOCKCYPHER_TOKEN
from schemas import BTCAddress, BTCTransaction


class BlockCypherBitcoinWrapper:
    api_token = BLOCKCYPHER_TOKEN
    api_url = "https://api.blockcypher.com/v1/btc/main" \
        if IS_PRODUCTION else "https://api.blockcypher.com/v1/btc/test3"

    blockcypher_wallet_name = "main"

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

        async with httpx.AsyncClient() as client:
            if request_type == "POST":
                if params:
                    url = urljoin(url, "?" + urlencode(params))

                resp = await client.post(url, json=data)

            else:
                resp = await client.get(url, params=params)

        return resp.json()

    async def create_wallet_address(self, quantity: int = 1) -> dict:
        endpoint = f"/wallets/hd/{self.blockcypher_wallet_name}/addresses/derive"
        return await self.request(endpoint, "GET", {"count": quantity}, with_token=True)

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
