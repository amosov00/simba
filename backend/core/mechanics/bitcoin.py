from typing import Union, Optional

from core.integrations.blockcypher import BlockCypherBitcoinWrapper
from database.crud import UserCRUD, BTCAddressCRUD
from schemas import User


class BitcoinWrapper:
    def __init__(self):
        self.blockcypher_wrapper = BlockCypherBitcoinWrapper()

    async def create_wallet_address(self, user: User):
        resp = await self.blockcypher_wrapper.create_wallet_address(1)
        if "errors" in resp:
            pass

        address = resp["chains"][0]["chain_addresses"][0]

        address_full_info = await self.blockcypher_wrapper.fetch_address_info(
            address.get("moSCLcuDoAvaMuMYza1XUydvkNH7dqxTEN")
        )
        address_full_info.user_id = user.id
        address_full_info.public_key = address.get("public")
        address_full_info.path = address.get("path")

        await BTCAddressCRUD.insert_one(address_full_info.dict())
        await UserCRUD.update_one({"_id": user.id}, {"btc_address": address_full_info.address})

        return address_full_info.address
