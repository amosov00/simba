from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request

from core.integrations.blockcypher import BlockCypherWebhooksWrapper

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get():
    return await BlockCypherWebhooksWrapper().list_webhooks()


@router.post("/")
async def debug_post():
    return {}
