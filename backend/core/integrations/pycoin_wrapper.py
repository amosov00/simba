import http
import random
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sentry_sdk import capture_message

from config import IS_PRODUCTION, BTC_COLD_WALLETS
from database.crud import BTCAddressCRUD, InvoiceCRUD, BTCxPubCRUD
from schemas import BTCAddress, User, InvoiceInDB, BTCxPub

if IS_PRODUCTION:
    from pycoin.symbols.btc import network
else:
    from pycoin.symbols.tbtx import network

__all__ = ["PycoinWrapper"]


class PycoinWrapper:
    def __init__(self, *, cold_wallet: BTCxPub = None, user: User = None, invoice: InvoiceInDB = None):
        self.cold_wallet: Optional[BTCxPub] = cold_wallet
        self.key = None
        self.user = user
        self.invoice = invoice

    @staticmethod
    def format_path(*indexes, include_m: bool = False) -> str:
        path = "/".join([str(i) for i in indexes])
        return path if not include_m else f"m/{path}"

    @staticmethod
    async def _created_address_is_valid(address: str):
        return not any([
            bool(await InvoiceCRUD.find_one({"target_btc_address": address})),
            bool(await BTCAddressCRUD.find_one({"address": address}))
        ])

    @classmethod
    async def from_active_xpub(cls, **kwargs) -> "PycoinWrapper":
        self = cls(**kwargs)
        active_xpubs = await BTCxPubCRUD.find_active()
        if not active_xpubs:
            raise ValueError("active xpub not exists")

        chosen_xpub = random.choice(active_xpubs)
        chosen_xpub = list(filter(lambda o: o.title == chosen_xpub.get("title"), BTC_COLD_WALLETS))
        self.cold_wallet = chosen_xpub[0] if chosen_xpub else None
        return self

    @staticmethod
    def _generate_subkey(key, path: str):
        return key.subkey_for_path(path)

    async def create_key(self):
        if not self.cold_wallet or not self.cold_wallet.xpub:
            capture_message("xpub from cold wallet is not found")
            raise HTTPException(http.HTTPStatus.INTERNAL_SERVER_ERROR, "xpub is not found")

        self.key = network.parse.bip32(self.cold_wallet.xpub.get_secret_value())
        return self.key

    async def _get_last_path_index(self, path: str):
        last_address = await BTCAddressCRUD.find_latest(self.cold_wallet.title, path)
        return last_address.get("path") if last_address else None

    async def _generate_new_path(self, path: list):
        last_path = await self._get_last_path_index(f"m/{path[0]}")

        if last_path:
            path_indexes = list(map(int, last_path.split("/")[1:] if "m" in last_path else last_path.split("/")))
            path_indexes[-1] = path_indexes[-1] + 1 + path[-1]
        else:
            path_indexes = path

        if len(path_indexes) < 2:
            path_indexes = path

        return self.format_path(*path_indexes)

    async def _save_address(self, address: str, path: str):
        assert path.startswith("m/")
        new_address = BTCAddress(
            user_id=self.user.id if self.user else None,
            invoice_id=self.invoice.id if self.invoice else None,
            address=address,
            path=path,
            balance=0,
            total_sent=0,
            total_received=0,
            n_tx=0,
            created_at=datetime.now(),
            cold_wallet_title=self.cold_wallet.title,
        )
        await BTCAddressCRUD.insert_one(new_address.dict())
        return True

    async def generate_new_address(self, *, path: int = 0, subpath: int = 0) -> str:
        await self.create_key()
        path_without_m = await self._generate_new_path([path, subpath])
        subkey = self._generate_subkey(self.key, path_without_m)
        created_address = subkey.address()
        if not await self._created_address_is_valid(created_address):
            return await self.generate_new_address(path=path, subpath=subpath + 1)

        await self._save_address(address=created_address, path="m/" + path_without_m)
        return created_address
