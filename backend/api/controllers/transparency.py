from typing import List, Literal

from fastapi import APIRouter, Query
from pydantic import parse_obj_as

from database.crud import BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD
from schemas import TransparencyTransaction, InvoiceStatus, InvoiceType, BTCTransactionOutputs, BTCAddressInDB
from core.mechanics import InvoiceMechanics
from config import BTC_COLD_WALLETS, BTC_HOT_WALLET_ADDRESS

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def transparency_totals():
    response = {}

    cold_wallets_meta = await BTCAddressCRUD.aggregate([
        {"$match": {"address": {"$ne": BTC_HOT_WALLET_ADDRESS}}},
        {"$group": {"_id": "$cold_wallet_title", "received": {"$sum": "$total_received"}}}
    ])

    total_recieved = sum([i["received"] for i in cold_wallets_meta])

    invoices_sell = await InvoiceCRUD.aggregate(
        [
            {"$match": {
                "status": InvoiceStatus.COMPLETED,
                "invoice_type": InvoiceType.SELL
            }},
            {"$group": {
                "_id": None,
                "btc_amount_proceeded": {"$sum": "$btc_amount_proceeded"},
            }},
        ]
    )
    total_paid_out = invoices_sell[0]["btc_amount_proceeded"] if invoices_sell else 0

    response.update(
        {
            "total_assets": total_recieved - total_paid_out,
            "total_recieved": total_recieved,
            "total_paid_out": total_paid_out,
        }
    )

    for cold_wallet in BTC_COLD_WALLETS:
        meta = list(filter(lambda o: o["_id"] == cold_wallet.title, cold_wallets_meta))
        received = meta[0].get("received") if meta else 0
        response.update({cold_wallet.title: {"received": received}})

    return response


@router.get("/transactions/", response_model=List[TransparencyTransaction])
async def transparency_transactions(
        tx_type: Literal["received", "paidout"] = Query(..., alias="type"),
):
    response = []
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
            target_btc_address = invoice["target_btc_address"] if tx_type == "received" else BTC_HOT_WALLET_ADDRESS

            if target_btc_address not in btc_tx["addresses"]:
                continue

            amount_from_outputs = InvoiceMechanics.get_incoming_btc_from_outputs(
                parse_obj_as(List[BTCTransactionOutputs], btc_tx["outputs"]), target_btc_address
            ) or 0

            response.append({
                "hash": btc_tx["hash"],
                "received": btc_tx["received"],
                "amount": amount_from_outputs if tx_type == "received" else btc_tx["total"] - amount_from_outputs
            })

    return response
