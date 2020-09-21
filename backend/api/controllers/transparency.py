from typing import Literal

from fastapi import APIRouter, Query

from core.mechanics import TransparencyMechanics
from database.crud import BTCAddressCRUD, BTCTransactionCRUD, InvoiceCRUD
from schemas import TransparencyTransactionResponse, InvoiceStatus, InvoiceType
from config import BTC_COLD_WALLETS

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def transparency_totals():
    return await TransparencyMechanics.fetch_common_info()


@router.get("/transactions/", response_model=TransparencyTransactionResponse)
async def transparency_transactions(
        tx_type: Literal["received", "paidout"] = Query(..., alias="type"),
):
    return await TransparencyMechanics.fetch_transactions(tx_type)
