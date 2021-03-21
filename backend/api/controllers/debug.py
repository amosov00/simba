from fastapi import APIRouter


from core.mechanics.invoices import rescue_stucked_invoices

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get():
    await rescue_stucked_invoices()
    return


@router.post("/")
async def debug_post():
    return {}
