from fastapi import APIRouter

from core.integrations.ethereum import EventsContractWrapper
from config import SIMBA_CONTRACT

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get():
    await EventsContractWrapper(SIMBA_CONTRACT).fetch_blocks_and_save()
    return


@router.post("/")
async def debug_post():
    return {}
