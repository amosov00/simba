from typing import Union, Optional, List

from pycoin.coins.tx_utils import create_signed_tx

from core.integrations.blockcypher import BlockCypherAPIWrapper
from database.crud import UserCRUD, BTCAddressCRUD
from schemas import User
from .base import CryptoValidation


class Payable:
    def __init__(self, address: str, amount: int):
        if not all([
            isinstance(address, str),
            isinstance(amount, int),
        ]):
            raise ValueError("Invalid types")

        self.address = address
        self.amount = amount

    @property
    def serialized(self) -> tuple:
        return self.address, self.amount


class BitcoinWrapper(CryptoValidation):
    def __init__(self):
        self.api_wrapper = BlockCypherAPIWrapper()

    @staticmethod
    def create_spendables(pairs=List[Payable]):
        result = []
        for pair in pairs:
            if not isinstance(pair, Payable):
                raise AttributeError("Invalid format of ")

            result.append(pair.serialized)
        return result

    async def create_and_sign_transaction(
            self,
            spendables: List[tuple],
            address_from: str,
            wifs: List[str],
            fee: Union[int, str] = "standard",
    ):

        payables = await self.api_wrapper.get_payables(address_from)

        tx = create_signed_tx(
            self.api_wrapper.network,
            spendables=spendables,
            payables=payables,
            wifs=wifs,
            fee=fee
        )
        return await self.api_wrapper.push_raw_tx(tx)

    async def create_wallet_address(self, user: User):
        resp = await self.api_wrapper.create_wallet_address(1)
        if "errors" in resp:
            pass

        address = resp["chains"][0]["chain_addresses"][0]
        address_full_info = await self.api_wrapper.fetch_address_info(
            address.get("address")
        )
        address_full_info.user_id = user.id
        address_full_info.public_key = address.get("public")
        address_full_info.path = address.get("path")

        await BTCAddressCRUD.insert_one(address_full_info.dict())
        await UserCRUD.update_one({"_id": user.id}, {"btc_address": address_full_info.address})

        return address_full_info.address
