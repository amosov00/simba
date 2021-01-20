from typing import Literal

from fastapi import APIRouter, Query

from core.mechanics import TransparencyMechanics
from core.utils import CustomJSONResponse
from schemas import TransparencyTransactionResponse

__all__ = ["router"]

router = APIRouter()


@router.get("/btc/")
async def transparency_totals():
    return await TransparencyMechanics.fetch_btc_common_info()


@router.get("/simba/")
async def transparency_totals():
    return await TransparencyMechanics.fetch_simba_common_info()


@router.get("/transactions/", response_model=TransparencyTransactionResponse)
async def transparency_transactions(
        tx_type: Literal["received", "paidout"] = Query(..., alias="type"),
):
    return await TransparencyMechanics.fetch_transactions(tx_type)
