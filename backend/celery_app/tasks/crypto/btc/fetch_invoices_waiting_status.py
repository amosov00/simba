from dateutil.parser import parse

from celery_app.celeryconfig import app
from database.crud import InvoiceCRUD, BTCAddressCRUD
from core.integrations.blockcypher import BlockCypherAPIWrapper
from schemas import InvoiceType, InvoiceStatus, InvoiceInDB, BTCAddressInDB

__all__ = ['invoice_waiting_status']


@app.task(
    name="invoice_waiting_status",
    bind=True,
    soft_time_limit=42,
    time_limit=300,
)
async def invoice_waiting_status(self, *args, **kwargs):
    invoices = await InvoiceCRUD.find_invoices_by_type_and_status(InvoiceType.BUY, InvoiceStatus.WAITING)
    for invoice in invoices:
        invoice = InvoiceInDB.parse_obj(invoice)
        old_address_data = BTCAddressInDB.parse_obj(await BTCAddressCRUD.find_by_address(invoice.target_btc_address))
        new_address_data = await BlockCypherAPIWrapper().fetch_address_info(invoice.target_btc_address)

        if old_address_data.balance == new_address_data.balance:
            continue
        else:
            # TODO большая уязвимость в подсчете, нужно будет потом это исправить
            balance_delta = new_address_data.balance - old_address_data.balance
            invoice.btc_amount_deposited += balance_delta

            if invoice.btc_amount_deposited >= invoice.btc_amount:
                invoice.status = InvoiceStatus.PROCESSING

            await BTCAddressCRUD.update_or_create(old_address_data.id, new_address_data.dict())
            await InvoiceCRUD.update_one(
                {"_id": invoice.id}, invoice.dict(include={"btc_amount_deposited", "status"})
            )

    return True


