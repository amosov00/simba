import asyncio, logging
from typing import List

from fastapi import APIRouter, Depends

from api.dependencies import get_user
from celery_app.tasks import fetch_empty_btc_addresses_info
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


@router.get("/refs/", response_model=ReferralInDB)
async def debug_get(user: User = Depends(get_user)):
    return await ReferralCRUD.find_by_user_id(user.id)


@router.get("/simba/")
async def debug_get():
    return None


@router.get("/sst/")
async def debug_get():
    inst = SSTWrapper(None)
    sst = 32 * 10**18
    period = 2500000
    tx = await inst._freeze_and_transfer(
        "0xeab67ecf3d5404fee42e18702f60b0e7defd269d", sst, period
    )
    print(tx)
    return None


@router.get("/btc/")
async def debug_get():
    return None


@router.get("/")
async def debug_get():
    return True


@router.post("/")
async def debug_post():
    return {}
