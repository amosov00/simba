from typing import Literal

from database.crud import BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD
from schemas import InvoiceStatus, InvoiceType
from config import BTC_COLD_WALLETS


class TransparencyMechanics:
    @classmethod
    async def fetch_xpubs_balance(cls) -> dict:
        xpub_meta = await BTCAddressCRUD.aggregate(
            [
                {"$match": {
                    "path": {"$regex": "m/(0|1)/"},
                }},
                {"$group": {
                    "_id": "$cold_wallet_title",
                    "balance": {"$sum": "$balance"},
                }},
            ]
        )
        return {
            i["_id"]: i["balance"] for i in xpub_meta if i["_id"]
        }

    @classmethod
    async def fetch_common_info(cls) -> dict:
        response = {
            "total_assets": 0,
            "total_recieved": 0,
            "total_paid_out": 0,
            **{wallet.title: 0 for wallet in BTC_COLD_WALLETS},
        }

        invoices_meta = await InvoiceCRUD.aggregate(
            [
                {"$match": {
                    "status": InvoiceStatus.COMPLETED,
                }},
                {"$group": {
                    "_id": "$invoice_type",
                    "btc_amount_proceeded": {"$sum": "$btc_amount_proceeded"},
                }},
            ]
        )
        response["total_recieved"] = list(
            filter(lambda o: o["_id"] == InvoiceType.BUY, invoices_meta)
        )[0]["btc_amount_proceeded"]
        response["total_paid_out"] = list(
            filter(lambda o: o["_id"] == InvoiceType.SELL, invoices_meta)
        )[0]["btc_amount_proceeded"]
        response["total_assets"] = response["total_recieved"] - response["total_paid_out"]

        response.update(await cls.fetch_xpubs_balance())

        return response

    @classmethod
    async def fetch_transactions(cls, tx_type: Literal["received", "paidout"]) -> dict:
        response = {
            "total": 0,
            "transactions": []
        }
        invoices = await InvoiceCRUD.aggregate(
            [
                {"$match": {
                    "status": InvoiceStatus.COMPLETED,
                    "invoice_type": InvoiceType.BUY if tx_type == "received" else InvoiceType.SELL,
                }},
                {"$lookup": {
                    "from": BTCTransactionCRUD.collection,
                    "localField": "_id",
                    "foreignField": "invoice_id",
                    "as": "btc_txs",
                }},
            ]
        )
        for invoice in invoices:
            for btc_tx in invoice["btc_txs"]:
                response["total"] += invoice["btc_amount_proceeded"]
                response["transactions"].append({
                    "hash": btc_tx["hash"],
                    "received": btc_tx["received"],
                    "amount": invoice["btc_amount_proceeded"]
                })

        return response
