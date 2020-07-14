import asyncio

from database.crud import BTCAddressCRUD
from config.crypto import BTC_COLD_XPUB_SWISS, BTC_HOT_WALLET_ADDRESS


async def main():
    await BTCAddressCRUD.update_many({"address": {"$ne": BTC_HOT_WALLET_ADDRESS}},
                                     {"cold_wallet_title": BTC_COLD_XPUB_SWISS.title})


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
