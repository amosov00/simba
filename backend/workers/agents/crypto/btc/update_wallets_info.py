import asyncio
import logging
from datetime import timedelta

from config import BTC_COLD_WALLETS
from core.integrations import PycoinWrapper
from core.mechanics import BitcoinWrapper
from database.crud import BTCAddressCRUD
from schemas import BTCxPub
from workers.agents import app

__all__ = ["update_btc_addresses_info_job"]

update_btc_addresses_info_topic = app.topic(
    "update_btc_addresses_info", internal=True, retention=timedelta(minutes=10), partitions=1
)


async def update_xpub_change_addresses(wallet: BTCxPub):
    inst = PycoinWrapper(cold_wallet=wallet)
    generated_address = await inst.generate_new_address(path=1, subpath=0)
    fetched_address = await BitcoinWrapper().fetch_address_and_save(generated_address)

    if fetched_address.transactions_number > 0:
        await asyncio.sleep(0.5)
        return await update_xpub_change_addresses(wallet)
    else:
        await BTCAddressCRUD.delete_one({"address": fetched_address.address})

    return True


async def update_existing_btc_addresses():
    counter = 0
    for address in await BTCAddressCRUD.find_many({"path": {"$regex": "m/(0|1)/"}}):
        await BitcoinWrapper().fetch_address_and_save(address.get("address"))
        counter += 1
        await asyncio.sleep(0.5)

    logging.info(f"Updated BTC addresses: {counter}")
    return


@app.agent(update_btc_addresses_info_topic, concurrency=1)
async def update_btc_addresses_info_job(stream):
    async for _ in stream:
        await update_existing_btc_addresses()

        for wallet in BTC_COLD_WALLETS:
            if not wallet.xpub:
                continue
            await update_xpub_change_addresses(wallet)
            logging.info(f"Fetched change addresses for {wallet.title}")

    return True
