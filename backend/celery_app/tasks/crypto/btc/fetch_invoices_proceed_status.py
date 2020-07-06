from celery_app.celeryconfig import app

from core.mechanics import BitcoinWrapper
from database.crud import InvoiceCRUD
from schemas import InvoiceInDB, BTCAddressInDB, InvoiceType, InvoiceStatus

__all__ = ['invoice_processing_status']


@app.task(
    name="invoice_waiting_status",
    bind=True,
    soft_time_limit=42,
    time_limit=300,
)
async def invoice_processing_status(self, *args, **kwargs):
    # TODO Complete, only SELL status
    invoices = await InvoiceCRUD.find_invoices_by_type_and_status(InvoiceType.SELL, InvoiceStatus.PROCESSING)
    for invoice in invoices:
        invoice = InvoiceInDB.parse_obj(invoice)
        # TODO make additional validation with transaction aggregation + md5 hash validation
        # result = await BitcoinWrapper().create_and_sign_transaction(
        #     spendables=[('spend')],
        #     address_from='from',
        #     wifs=['wif'],
        #     test=True,
        # )


    return True
