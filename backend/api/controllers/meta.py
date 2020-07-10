from fastapi import APIRouter, HTTPException, Depends, Body, Path
import ujson
import logging

from sentry_sdk import capture_message
from api.dependencies import get_user
from core.mechanics import InvoiceMechanics
from database.crud import BlockCypherWebhookCRUD, InvoiceCRUD
from schemas import EthereumContract, BTCTransaction
from config import SIMBA_CONTRACT, SIMBA_ADMIN_ADDRESS

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


@router.get(
    "/eth/admin-address/",
    dependencies=[Depends(get_user), ],
    responses={
        200: {
            "description": "Return Simba admin address",
            "content": {
                "application/json": {
                    "example": {"address": "0x....."}
                }
            },
        },
    },
)
async def meta_simba_admin_address():
    return {"address": SIMBA_ADMIN_ADDRESS}


@router.post("/{webhook_path}/", include_in_schema=False)
async def meta_webhook_handler(
        webhook_path: str = Path(...), transaction: dict = Body(...),
):
    webhook_obj = await BlockCypherWebhookCRUD.find_one({"url_path": webhook_path})
    invoice = await InvoiceCRUD.find_one({"_id": webhook_obj["invoice_id"]}) if webhook_obj else None

    if webhook_obj and invoice:
        transaction = BTCTransaction(**transaction)
        await InvoiceMechanics(invoice).proceed_new_transaction(transaction)
    else:
        capture_message("Webhook obj or invoice not found", level="error")

    return True
