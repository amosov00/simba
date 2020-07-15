from celery_app.celeryconfig import app
from database.crud import BTCAddressCRUD, InvoiceCRUD
from schemas import BTCAddressInDB, InvoiceStatus
from core.mechanics import BitcoinWrapper

__all__ = ["update_empty_btc_addresses_info"]


@app.task(
    name="update_empty_btc_addresses_info", bind=True, soft_time_limit=42, time_limit=300,
)
async def update_empty_btc_addresses_info(self, *args, **kwargs):
    """Обновление данных кошельков BTC для статистики в transparency"""
    btc_addresses = await BTCAddressCRUD.find_many({"transactions_number": 0, "fetch_address": {"$ne": False}})
    for btc_address in btc_addresses:
        old_btc_address_data = BTCAddressInDB(**btc_address)
        new_btc_address_data = await BitcoinWrapper().fetch_address_and_save(
            address=old_btc_address_data.address,
            invoice_id=old_btc_address_data.invoice_id,
            user_id=old_btc_address_data.user_id,
            save=False,
        )
        if new_btc_address_data.transactions_number != old_btc_address_data.transactions_number:
            new_btc_address_data.fetch_address = False
            await BTCAddressCRUD.update_one({"_id": old_btc_address_data.id}, new_btc_address_data.dict())
        else:
            linked_invoice = await InvoiceCRUD.find_one({"_id": old_btc_address_data.invoice_id})

            if not linked_invoice or (
                linked_invoice and linked_invoice.get("status") == InvoiceStatus.CANCELLED
            ):
                await BTCAddressCRUD.update_one({"_id": old_btc_address_data.id}, {"fetch_address": False})

    return True
