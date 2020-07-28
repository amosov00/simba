from datetime import datetime
from typing import Optional

from pycoin.coins.Tx import Tx

from schemas import BTCAddress, BTCTransaction
from .base import BlockCypherBaseAPIWrapper


class BlockCypherAPIWrapper(BlockCypherBaseAPIWrapper):
    async def create_wallet_address(self, quantity: int = 1) -> dict:
        endpoint = f"/wallets/hd/{self.blockcypher_wallet_name}/addresses/derive"
        return await self.request(endpoint, "POST", {"count": quantity}, with_token=True)

    async def fetch_address_info(self, address_hash: str) -> Optional[BTCAddress]:
        endpoint = f"/addrs/{address_hash}/"
        res = await self.request(endpoint, with_token=True)
        return BTCAddress(**res) if res else None

    async def fetch_transaction_info(self, transaction_hash: str) -> Optional[BTCTransaction]:
        endpoint = f"/txs/{transaction_hash}/"
        res = await self.request(endpoint, params={"limit": 50})
        if not res:
            pass
        return BTCTransaction(**res) if res else None

    async def create_transaction(self, data: dict) -> dict:
        endpoint = f"/txs/new/"
        res = await self.request(endpoint, request_type="POST", data=data)
        return res

    async def send_transaction(self, data: dict):
        endpoint = f"/txs/send/"
        res = await self.request(endpoint, request_type="POST", data=data, with_token=True)
        return res

    async def current_balance(self, address: str):
        endpoint = f"/addrs/{address}/"
        res = await self.request(endpoint, request_type="GET")
        return res.get("final_balance")

    async def push_raw_tx(self, tx: Tx):
        return self.broadcast_tx(tx)

    async def get_spendables(self, address: str):
        return self.spendables_for_address(address)
