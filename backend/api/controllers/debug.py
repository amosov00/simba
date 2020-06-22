from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request

from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper, BlockCypherAPIWrapper
from core.mechanics import BitcoinWrapper, BlockCypherWebhookHandler, SimbaWrapper, BitcoinWrapper, SSTWrapper
from database.crud import InvoiceCRUD
from schemas import InvoiceInDB, BlockCypherWebhookEvents, InvoiceUpdate
from celery_app.tasks import debug_task_1
from bson import ObjectId

__all__ = ["router"]

router = APIRouter()


@router.get("/webhooks/")
async def debug_get():
    return await BlockCypherWebhookAPIWrapper().list_webhooks()


@router.get("/")
async def debug_get():
    # hash_ = await SimbaWrapper().validate_and_issue_tokens(None, "0xd69401E5B2F93EB66E585711ec4CEFD6e8C8346D", 1000, "test")
    # return hash_
    return True

    # res = await BitcoinWrapper().create_and_sign_transaction(
    #     [("myWxTnrj3UHr9HQ9gzSpse7nm9vpdp47to", 72000)],
    #     "n4JC3GyL8VrFw9KVLGgHkbRkn2HvCCFMy4",
    #     ["cNEmkPzK18zuqV771NWxo5VQdYadbTJ1i4ExsuKjCGJguKEd9XrX"],
    # )
    # breakpoint()
    # return await BlockCypherAPIWrapper().current_balance("n4JC3GyL8VrFw9KVLGgHkbRkn2HvCCFMy4")
    # invoice = InvoiceInDB(**await InvoiceCRUD.find_by_id(ObjectId("5eec5ab7e195de21290c5a91")))
    #
    # return await BlockCypherWebhookHandler().create_webhook(
    #     invoice, BlockCypherWebhookEvents.TX_CONFIMATION, wallet_address="mqS8WqAw6Q7a8zoTj1H52TprweYEeeUdc4"
    # )


@router.post("/")
async def debug_post():
    return {}
