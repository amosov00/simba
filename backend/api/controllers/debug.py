from typing import List

import asyncio
from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request

from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper, BlockCypherAPIWrapper
from core.mechanics.crypto import SimbaWrapper
from celery_app.tasks import delete_unused_webhooks, finish_overdue_invoices
from database.crud import InvoiceCRUD, BlockCypherWebhookCRUD, ReferralCRUD
from schemas import BlockCypherWebhookInDB, User, ReferralInDB, InvoiceInDB
from api.dependencies import get_user

__all__ = ["router"]

router = APIRouter()


@router.get("/cron/")
async def debug_get():
    return await finish_overdue_invoices()


@router.get("/invoices/", response_model=List[InvoiceInDB])
async def debug_get():
    return await InvoiceCRUD.find_many({})


@router.get("/webhooks/", response_model=List[BlockCypherWebhookInDB])
async def debug_get():
    return await BlockCypherWebhookCRUD.find_many({})


@router.get("/refs/", response_model=ReferralInDB)
async def debug_get(user: User = Depends(get_user)):
    return await ReferralCRUD.find_by_user_id(user.id)


# @router.get("/eth/")
# async def debug_get():
#     return await SimbaWrapper().issue_tokens(
#         "0xbeb3ec5bce587420c00ec547ca2dd5626f497b73",
#         100000,
#         "manual-test"
#     )


@router.get("/")
async def debug_get():
    await delete_unused_webhooks.delay()
    return True


@router.post("/")
async def debug_post():
    return {}
