from typing import List

import asyncio
from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request

from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper, BlockCypherAPIWrapper
from core.mechanics.crypto import SimbaWrapper
from database.crud import InvoiceCRUD, BlockCypherWebhookCRUD, ReferralCRUD
from schemas import BlockCypherWebhookInDB, User, ReferralInDB
from api.dependencies import get_user
from celery_app.tasks import delete_unused_webhooks

__all__ = ["router"]

router = APIRouter()


@router.get("/webhooks/")
async def debug_get():
    return await BlockCypherWebhookAPIWrapper().list_webhooks()


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
