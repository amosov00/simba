import asyncio
from typing import List

from fastapi import APIRouter, Depends

from api.dependencies import get_user
from celery_app.tasks import fetch_empty_btc_addresses_info, delete_unused_webhooks
from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper
from core.mechanics.crypto import SimbaWrapper, SSTWrapper, BitcoinWrapper
from database.crud import InvoiceCRUD, BlockCypherWebhookCRUD, ReferralCRUD
from schemas import BlockCypherWebhookInDB, User, ReferralInDB, InvoiceInDB

__all__ = ["router"]

router = APIRouter()


@router.get("/cron/")
async def debug_get():
    await fetch_empty_btc_addresses_info()
    return True


@router.get("/invoices/", response_model=List[InvoiceInDB])
async def debug_get():
    return await InvoiceCRUD.find_many({})


@router.get("/webhooks/", response_model=List[BlockCypherWebhookInDB])
async def debug_get():
    return await BlockCypherWebhookCRUD.find_many({})


@router.delete("/webhooks/")
async def debug_get():
    hooks = await BlockCypherWebhookAPIWrapper().list_webhooks()
    for hook in hooks:
        await BlockCypherWebhookAPIWrapper().delete_webhook(hook["id"])
        await asyncio.sleep(0.5)

    return True


@router.get("/refs/", response_model=ReferralInDB)
async def debug_get(user: User = Depends(get_user)):
    return await ReferralCRUD.find_by_user_id(user.id)


@router.get("/simba/")
async def debug_get():
    result = await SimbaWrapper().redeem_tokens(
        100000, "e3a671d13607f8512806851e78d92341c33b1efd16093a707d39e95a04cee3a1"
    )
    print(f"SIMBA {result}")
    return None


@router.get("/sst/")
async def debug_get():
    await asyncio.sleep(15.0)
    result = SSTWrapper().api_wrapper.freeze_and_transfer(
        "0xBeb3EC5BCE587420c00eC547cA2DD5626f497B73", 15, 250000
    )
    print(f"SST {result.hex()}")
    return None


@router.get("/btc/")
async def debug_get():
    res = await BitcoinWrapper().create_and_sign_transaction("mgcEs8CPgX1uJjjyLRbv4vLVuabevKe9LE", 72544)
    return None


@router.get("/")
async def debug_get():
    return True


@router.post("/")
async def debug_post():
    return {}
