from typing import List

import httpx
from fastapi import APIRouter, Depends

from api.dependencies import get_user
from celery_app.tasks import rescue_stucked_invoices
from database.crud import InvoiceCRUD, BlockCypherWebhookCRUD, ReferralCRUD
from schemas import BlockCypherWebhookInDB, User, ReferralInDB, InvoiceInDB

__all__ = ["router"]

router = APIRouter()


@router.get("/cron/")
async def debug_get():
    return await rescue_stucked_invoices(None)


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
    return None


@router.get("/btc/")
async def debug_get():
    return None


@router.get("/")
async def debug_get():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post("http://backend-nodejs:8080/api/multisig", data={})
            resp = resp.json()
        except Exception as e:
            resp = str(e)

    return resp


@router.post("/")
async def debug_post():
    return {}
