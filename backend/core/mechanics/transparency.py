from datetime import datetime, timedelta
from typing import Literal

from bson import Decimal128

from config import BTC_COLD_WALLETS, SIMBA_CONTRACT
from core.integrations.ethereum.base_wrapper import EthereumBaseContractWrapper
from database.crud import BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD, MetaCRUD, EthereumTransactionCRUD
from schemas import InvoiceStatus, InvoiceType, MetaSlugs, SimbaContractEvents


class TransparencyMechanics:
    @classmethod
    async def fetch_blacklisted_balance(cls) -> int:
        obj = await MetaCRUD.find_by_slug(MetaSlugs.BLACKLISTED_BALANCE, raise_404=False) or {}
        return obj.get("payload", {}).get("balance", 0)

    @classmethod
    async def fetch_simba_meta(cls) -> dict:
        obj = await MetaCRUD.find_by_slug(MetaSlugs.SIMBA_META, raise_404=False) or {}
        resp = {"holders": 0, "totalAssets": 0}

        if obj and obj.get("payload") and obj["updated_at"] > datetime.now() - timedelta(hours=6):
            resp["holders"] = obj["payload"].get("holdersCount")
            resp["totalAssets"] = obj["payload"].get("totalSupply")

        else:
            holders = await EthereumTransactionCRUD.aggregate(
                [
                    {"$match": {"contract": "SIMBA", "event": SimbaContractEvents.Transfer}},
                    {"$replaceRoot": {"newRoot": "$args"}},
                    {"$project": {"to": 1}},
                ]
            )
            resp["holders"] = len({i["to"] for i in holders})
            try:
                resp["totalAssets"] = (
                    EthereumBaseContractWrapper(SIMBA_CONTRACT).contract.functions.totalSupply().call()
                )
            except Exception:
                resp["totalAssets"] = 0

        return resp

    @classmethod
    async def fetch_xpubs_balance(cls) -> dict:
        xpub_meta = await BTCAddressCRUD.aggregate(
            [
                {
                    "$match": {
                        "path": {"$regex": "m/(0|1)/"},
                    }
                },
                {
                    "$group": {
                        "_id": "$cold_wallet_title",
                        "balance": {"$sum": "$balance"},
                    }
                },
            ]
        )
        return {i["_id"]: i["balance"] for i in xpub_meta if i["_id"]}

    @classmethod
    async def fetch_simba_common_info(cls) -> dict:
        amounts = {
            "quarantined": await cls.fetch_blacklisted_balance(),
            "circulation": 0,
        }
        for i in await EthereumTransactionCRUD.aggregate(
            [
                {
                    "$match": {
                        "contract": "SIMBA",
                        "event": {"$in": [SimbaContractEvents.OnIssued, SimbaContractEvents.OnRedeemed]},
                    }
                },
                {
                    "$group": {
                        "_id": "$event",
                        "value": {"$sum": "$args.value"},
                    }
                },
            ]
        ):
            if isinstance(i["value"], Decimal128):
                amounts[i["_id"]] = int(i["value"].to_decimal())
            else:
                amounts[i["_id"]] = int(i["value"])

        amounts["circulation"] = (
            amounts[SimbaContractEvents.OnIssued] - amounts[SimbaContractEvents.OnRedeemed] - amounts["quarantined"]
        )

        return {**amounts, **await cls.fetch_simba_meta()}

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
                {
                    "$match": {
                        "status": InvoiceStatus.COMPLETED,
                    }
                },
                {
                    "$group": {
                        "_id": "$invoice_type",
                        "btc_amount_proceeded": {"$sum": "$btc_amount_proceeded"},
                    }
                },
            ]
        )
        response["total_recieved"] = list(filter(lambda o: o["_id"] == InvoiceType.BUY, invoices_meta))[0][
            "btc_amount_proceeded"
        ]
        response["total_paid_out"] = list(filter(lambda o: o["_id"] == InvoiceType.SELL, invoices_meta))[0][
            "btc_amount_proceeded"
        ]
        response["total_assets"] = response["total_recieved"] - response["total_paid_out"]

        response.update(await cls.fetch_xpubs_balance())

        return response

    @classmethod
    async def fetch_transactions(cls, tx_type: Literal["received", "paidout", "all"]) -> dict:
        response = {"total": 0, "transactions": []}

        pipeline = [
            {
                "$match": {
                    "status": InvoiceStatus.COMPLETED,
                }
            },
            {"$sort": {"created_at": -1}},
            {
                "$lookup": {
                    "from": BTCTransactionCRUD.collection,
                    "localField": "_id",
                    "foreignField": "invoice_id",
                    "as": "btc_txs",
                }
            },
        ]

        if tx_type == "received":
            pipeline[0]["$match"]["invoice_type"] = InvoiceType.BUY
        elif tx_type == "paidout":
            pipeline[0]["$match"]["invoice_type"] = InvoiceType.SELL

        invoices = await InvoiceCRUD.aggregate(pipeline)

        for invoice in invoices:
            if len(invoice["btc_txs"]) == 0:
                continue
            else:
                btc_tx = invoice["btc_txs"][0]
                if tx_type == "all":
                    if invoice["invoice_type"] == InvoiceType.SELL:
                        amount = invoice["btc_amount_proceeded"] * -1
                    else:
                        amount = invoice["btc_amount_proceeded"]
                else:
                    amount = invoice["btc_amount_proceeded"]

                response["total"] += amount
                response["transactions"].append(
                    {"hash": btc_tx["hash"], "received": btc_tx["received"], "amount": amount}
                )

        response["transactions"] = sorted(response["transactions"], key=lambda o: ["received"], reverse=True)

        return response
