import asyncio
import json
from datetime import datetime, timedelta, timezone

from pymongo.results import InsertOneResult

from database.crud import InvoiceCRUD, BTCAddressCRUD, BTCTransactionCRUD, UserCRUD
from schemas import Invoice, InvoiceInDB, BTCAddress, BTCTransaction, Invoice, InvoiceType, InvoiceStatus, User
from core.mechanics import BitcoinWrapper
from config import SIMBA_BUY_SELL_FEE, BTC_COLD_XPUB_SWISS


def read_json() -> list:
    with open("txs_data.json") as f:
        lines = json.load(f)
        f.close()

    return lines["transactions"]


async def main():
    user = await UserCRUD.find_by_id("5f0305ec82d012e05bd6346a")
    user = User(**user)
    txs = read_json()
    counter = 0

    for transaction in txs:
        amount = int(transaction["amount"] * 10 ** 8)
        created_time = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        finised_time = created_time + timedelta(hours=2)
        invoice = Invoice(
            user_id=user.id,
            status=InvoiceStatus.COMPLETED,
            invoice_type=InvoiceType.BUY,
            btc_amount=amount,
            simba_amount=amount - SIMBA_BUY_SELL_FEE,
            btc_amount_proceeded=amount,
            simba_amount_proceeded=amount - SIMBA_BUY_SELL_FEE,
            target_eth_address="",
            target_btc_address=transaction["address"],
            eth_tx_hashes=[],
            btc_tx_hashes=[transaction["hash"]],
            sst_tx_hashes=[],
            created_at=created_time,
            finised_at=finised_time,
        )
        res: InsertOneResult = await InvoiceCRUD.insert_one(invoice.dict())
        invoice_id = res.inserted_id

        btc_address = BTCAddress(
            user_id=user.id,
            invoice_id=invoice_id,
            address=transaction["address"],
            created_at=created_time,
            cold_wallet_title=BTC_COLD_XPUB_SWISS.title,
        )
        await BTCAddressCRUD.insert_one(btc_address.dict())
        btc_tx = await BitcoinWrapper().fetch_transaction(transaction["hash"])
        btc_tx.invoice_id = invoice_id
        btc_tx.simba_tokens_issued = True
        await BTCTransactionCRUD.insert_one(btc_tx.dict())

        await asyncio.sleep(0.5)

    print(f"Finished, fetched {counter} txs")
    return None


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
