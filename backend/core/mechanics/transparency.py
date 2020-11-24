from typing import Literal

from bson import Decimal128

from config import BTC_COLD_WALLETS, SIMBA_CONTRACT
from core.integrations.ethereum.base_wrapper import EthereumBaseContractWrapper
from database.crud import BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD, MetaCRUD, EthereumTransactionCRUD
from schemas import InvoiceStatus, InvoiceType, MetaSlugs, SimbaContractEvents


class TransparencyMechanics:
    @classmethod
    async def fetch_blacklisted_balance(cls) -> int:
        inst = await MetaCRUD.find_by_slug(MetaSlugs.BLACKLISTED_BALANCE, raise_404=False) or {}
        return inst.get("payload", {}).get("balance", 0)

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
    async def fetch_simba_common_info(cls) -> dict:
        amounts = {
            "quarantined": await cls.fetch_blacklisted_balance()
        }
        for i in await EthereumTransactionCRUD.aggregate([
            {"$match": {
                "contract": "SIMBA",
                "event": {"$in": [SimbaContractEvents.OnIssued, SimbaContractEvents.OnRedeemed]}
            }},
            {"$group": {
                "_id": "$event",
                "value": {"$sum": "$args.value"},
            }},
        ]):
            if isinstance(i["value"], Decimal128):
                amounts[i["_id"]] = int(i["value"].to_decimal())
            else:
                amounts[i["_id"]] = int(i["value"])

        holders = await EthereumTransactionCRUD.aggregate([
            {"$match": {
                "contract": "SIMBA",
                "event": SimbaContractEvents.Transfer
            }},
            {"$replaceRoot": {"newRoot": "$args"}},
            {"$project": {"to": 1}},
        ])
        holders = len(set([i["to"] for i in holders]))
        try:
            total_supply = EthereumBaseContractWrapper(SIMBA_CONTRACT).contract.functions.totalSupply().call()
        except Exception:
            total_supply = 0
        circulation = amounts[SimbaContractEvents.OnIssued] \
                      - amounts[SimbaContractEvents.OnRedeemed] \
                      - amounts["quarantined"]
        return {
            "holders": holders,
            "totalAssets": total_supply,
            "circulation": circulation,
            **amounts
        }

    @classmethod
    async def fetch_btc_common_info(cls) -> dict:
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
                {"$sort": {
                    "created_at": -1
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
