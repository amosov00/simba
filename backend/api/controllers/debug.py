from fastapi import APIRouter


from bson import ObjectId
from schemas import InvoiceInDB
from database.crud import InvoiceCRUD
from core.utils.email import Email

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
