from typing import List, Optional, Literal
from os import environ
from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request


__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get(
    request: Request,
):
    return {
    }


@router.post("/")
async def debug_post():
    return {}
