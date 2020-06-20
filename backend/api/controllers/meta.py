from fastapi import APIRouter, HTTPException, Depends, Body, Path
import ujson
import logging

from api.dependencies import get_user
from core.mechanics import BlockCypherWebhookHandler
from database.crud import BlockCypherWebhookCRUD
from schemas import EthereumContract
from config import SIMBA_CONTRACT

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


@router.post("/{webhook_path}/", include_in_schema=False)
async def meta_webhook_handler(
        webhook_path: str = Path(...),
        payload: dict = Body(...),
):
    logging.info(payload)
    webhook_obj = await BlockCypherWebhookCRUD.find_one({"url_path": webhook_path})

    if webhook_obj:
        await BlockCypherWebhookHandler().parse(payload)

    return True
