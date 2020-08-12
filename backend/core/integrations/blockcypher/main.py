from typing import Optional, Union

from pycoin.coins.Tx import Tx

from schemas import BTCAddress, BTCTransaction
from .base import BlockCypherBaseAPIWrapper


class BlockCypherAPIWrapper(BlockCypherBaseAPIWrapper):
    async def create_wallet_address(self, quantity: int = 1) -> dict:
        endpoint = f"/wallets/hd/{self.blockcypher_wallet_name}/addresses/derive"
        return await self.request(endpoint, "POST", {"count": quantity}, with_token=True)

    async def fetch_address_info(self, address_hash: str) -> Optional[BTCAddress]:
        endpoint = f"/addrs/{address_hash}"
        res = await self.request(endpoint, with_token=True)
        return BTCAddress(**res) if res else None

    async def fetch_transaction_info(self, transaction_hash: str) -> Optional[BTCTransaction]:
        endpoint = f"/txs/{transaction_hash}"
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
        endpoint = f"/addrs/{address}"
        res = await self.request(endpoint, request_type="GET")
        return res.get("final_balance")

    async def decode_tx(self, tx: Union[str, Tx]):
        if isinstance(tx, Tx):
            tx = tx.as_hex()

        endpoint = "/txs/decode"
        data = {"tx": tx}
        resp = await self.request(endpoint, request_type="POST", data=data, with_token=False)
        return BTCTransaction(**resp) if resp else None

    async def push_raw_tx(self, tx: Union[str, Tx]):
        if isinstance(tx, Tx):
            tx = tx.as_hex()

        endpoint = "/txs/push"
        data = {"tx": tx}
        resp = await self.request(endpoint, request_type="POST", data=data, with_token=False)
        return BTCTransaction(**resp) if resp else None

    async def get_spendables(self, address: str):
        return [i.as_dict() for i in self.spendables_for_address(address)]
