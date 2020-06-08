import asyncio

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request

from database.crud import DebugCRUD

from celery_app.tasks import debug_task_1


__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get():
    # await debug_task_1.delay()
    res = await DebugCRUD.find_many({})
    for i in res:
        i.pop("_id", None)
    return res


@router.post("/")
async def debug_post():
    return {}
