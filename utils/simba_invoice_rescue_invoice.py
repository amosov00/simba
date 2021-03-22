import asyncio

from core.mechanics.crypto import BitcoinWrapper
from core.mechanics.invoices import InvoiceMechanics
from database.crud import InvoiceCRUD, UserCRUD
from schemas import InvoiceStatus, InvoiceInDB

INVOICE_ID = ""
TX_HASH = ""


# Use then invoice is cancelled, btc tx not in db, invoice is BUY
async def main():
    invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(INVOICE_ID))
    user = await UserCRUD.find_by_id(invoice.id)

    tx = await BitcoinWrapper().fetch_transaction(TX_HASH)
    print("Got tx ", tx.hash, " with confirmations ", tx.confirmations)

    invoice.status = InvoiceStatus.WAITING

    await InvoiceMechanics(invoice, user).proceed_new_transaction(tx)

    print("Done")


asyncio.get_event_loop().run_until_complete(main())
