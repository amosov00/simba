from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request
import ujson

from api.dependencies import get_user
from core.mechanics import BlockCypherWebhookHandler
from schemas import EthereumContract
from config import SIMBA_CONTRACT, WEBHOOK_PATH

__all__ = ["router"]

router = APIRouter()


@router.get(
    "/eth/contract/",
    dependencies=[Depends(get_user), ],
    response_model=EthereumContract,
    response_model_exclude={"abi_filepath"},
)
async def meta_contract_fetch():
    contract = SIMBA_CONTRACT

    with open(contract.abi_filepath) as f:
        abi = ujson.load(f)
        contract.abi = abi

    return contract


@router.post(f"/{WEBHOOK_PATH}/")
async def meta_webhook_handler(
        payload: dict = Body(...)
):
    await BlockCypherWebhookHandler().parse(payload)
    return {"success": True}
