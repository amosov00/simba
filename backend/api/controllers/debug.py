from fastapi import APIRouter


from bson import ObjectId
from schemas import InvoiceInDB
from database.crud import InvoiceCRUD
from core.utils.email import Email

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get():
    invoice = await InvoiceCRUD.find_one({"_id": ObjectId("6054a002194575326398518d")})
    await Email().new_suspended_invoice(invoice=InvoiceInDB(**invoice))
    return


@router.post("/")
async def debug_post():
    return {}
