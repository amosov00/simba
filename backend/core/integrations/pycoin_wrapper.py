from datetime import datetime

from config import IS_PRODUCTION, BTC_COLD_XPUB_SWISS
from database.crud import BTCAddressCRUD, InvoiceCRUD
from schemas import BTCAddress, User, InvoiceInDB, BTCXPUB

if IS_PRODUCTION:
    from pycoin.symbols.btc import network
else:
    from pycoin.symbols.tbtx import network

__all__ = ["PycoinWrapper"]


class PycoinWrapper:
    def __init__(self, *, user: User, invoice: InvoiceInDB):
        self.cold_wallet = self._get_cold_wallet()
        assert self.cold_wallet.xpub is not None

        self.key = network.parse.bip32(self.cold_wallet.xpub)
        self.user = user or None
        self.invoice = invoice or None

    @staticmethod
    def format_path(*indexes, include_m: bool = False) -> str:
        path = "/".join([str(i) for i in indexes])
        return path if not include_m else f"m/{path}"

    @staticmethod
    def _get_cold_wallet() -> BTCXPUB:
        return BTC_COLD_XPUB_SWISS

    @staticmethod
    async def _created_address_is_valid(address: str):
        return not any([
            bool(await InvoiceCRUD.find_one({"target_btc_address": address})),
            bool(await BTCAddressCRUD.find_one({"address": address}))
        ])

    @staticmethod
    async def _get_last_path_index():
        last_address = await BTCAddressCRUD.find_latest()
        return last_address.get("path") if last_address else None

    def _generate_subkey(self, path: str):
        return self.key.subkey_for_path(path)

    async def _generate_new_path(self, shift: int = 0):
        last_path = await self._get_last_path_index()

        if last_path:
            path_indexes = last_path.split("/")[1:] if "m" in last_path else last_path.split("/")
        else:
            path_indexes = ["0", "1"]

        if len(path_indexes) < 2:
            path_indexes = ["0", "1"]

        path_indexes[-1] = str(int(path_indexes[-1]) + 1 + shift)

        return self.format_path(*path_indexes)

    async def _save_address(self, address: str, path: str):
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

    async def generate_new_address(self, *, shift: int = 0) -> str:
        path_without_m = await self._generate_new_path(shift)
        path_with_m = "m/" + path_without_m
        key = self._generate_subkey(path_without_m)
        created_address = key.address()
        if not await self._created_address_is_valid(created_address):
            return await self.generate_new_address(shift=shift + 1)
        await self._save_address(address=created_address, path=path_with_m)
        return created_address
