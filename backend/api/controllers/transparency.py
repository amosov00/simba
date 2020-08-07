from typing import Literal

from fastapi import APIRouter, Query

from database.crud import BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD
from schemas import TransparencyTransactionResponse, InvoiceStatus, InvoiceType
from config import BTC_COLD_WALLETS

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def transparency_totals():
    response = {
        "total_assets": 0,
        "total_recieved": 0,
        "total_paid_out": 0,
        **{wallet.title: 0 for wallet in BTC_COLD_WALLETS}
    }

    invoices_buy = await InvoiceCRUD.aggregate(
        [
            {"$match": {
                "status": InvoiceStatus.COMPLETED,
                "invoice_type": InvoiceType.BUY,
            }},
            {"$lookup": {
                "from": BTCAddressCRUD.collection,
                "localField": "target_btc_address",
                "foreignField": "address",
                "as": "btc_address_obj",
            }},
        ]
    )
    for invoice in invoices_buy:
        response["total_recieved"] += invoice["btc_amount_proceeded"] if invoice.get("btc_amount_proceeded") else 0
        if invoice["btc_address_obj"]:
            cold_wallet_title = invoice["btc_address_obj"][0]["cold_wallet_title"]
            if cold_wallet_title in response.keys():
                response[cold_wallet_title] += invoice["btc_amount_proceeded"]

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
    response["total_paid_out"] = invoices_sell[0]["btc_amount_proceeded"] if invoices_sell else 0
    response["total_assets"] = response["total_recieved"] - response["total_paid_out"]

    return response


@router.get("/transactions/", response_model=TransparencyTransactionResponse)
async def transparency_transactions(
        tx_type: Literal["received", "paidout"] = Query(..., alias="type"),
):
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
