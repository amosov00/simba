import asyncio
import logging
from datetime import timedelta

from core.mechanics.crypto import BitcoinWrapper
from database.crud import BTCAddressCRUD, InvoiceCRUD
from schemas import BTCAddressInDB, InvoiceStatus
from workers.agents import app

__all__ = ["update_empty_btc_addresses_info_job"]

update_empty_btc_addresses_info_topic = app.topic(
    "update_empty_btc_addresses_info", internal=True, retention=timedelta(minutes=10), partitions=1
)


@app.agent(update_empty_btc_addresses_info_topic, concurrency=1)
async def update_empty_btc_addresses_info_job(stream):
    """Обновление данных кошельков BTC для статистики в transparency."""
    async for _ in stream:
        counter = 0
        btc_addresses = await BTCAddressCRUD.find_many({"transactions_number": 0, "fetch_address": {"$ne": False}})

        for btc_address in btc_addresses:
            old_btc_address_data = BTCAddressInDB(**btc_address)
            new_btc_address_data = await BitcoinWrapper().fetch_address_and_save(
                address=old_btc_address_data.address,
                invoice_id=old_btc_address_data.invoice_id,
                user_id=old_btc_address_data.user_id,
                save=False,
            )
            if not new_btc_address_data:
                await BTCAddressCRUD.update_one({"_id": old_btc_address_data.id}, {"fetch_address": False})
                continue

            if new_btc_address_data.transactions_number != old_btc_address_data.transactions_number:
                new_btc_address_data.fetch_address = False

                await BTCAddressCRUD.update_one(
                    {"_id": old_btc_address_data.id},
                    new_btc_address_data.dict(exclude_defaults=True, exclude_unset=True),
                )
                counter += 1
            else:
                linked_invoice = await InvoiceCRUD.find_one({"_id": old_btc_address_data.invoice_id})

                if new_btc_address_data.transactions_number == 0 and (
                    linked_invoice and linked_invoice.get("status") == InvoiceStatus.CANCELLED
                ):
                    new_btc_address_data.fetch_address = False
                    await BTCAddressCRUD.update_one(
                        {"_id": old_btc_address_data.id},
                        new_btc_address_data.dict(exclude_defaults=True, exclude_unset=True),
                    )

            # Wait to bypass blockcypher limitation
            await asyncio.sleep(1)

        if counter:
            logging.info(f"Updated {counter} btc wallets")

    return
