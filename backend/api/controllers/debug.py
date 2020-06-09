import asyncio

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request

from database.crud import DebugCRUD

from celery_app.tasks import debug_task_1


__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get():
    try:
        res = await asyncio.wait_for(debug_task_1.apply_async(), timeout=2)
    except asyncio.TimeoutError:
        res = "Timeout"
    return {"res": res}


@router.post("/")
async def debug_post():
    return {}
