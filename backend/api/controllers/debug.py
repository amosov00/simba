from typing import List

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request

from core.integrations.blockcypher import BlockCypherWebhookAPIWrapper, BlockCypherAPIWrapper
from core.mechanics.crypto import SimbaWrapper
from database.crud import InvoiceCRUD, BlockCypherWebhookCRUD
from schemas import BlockCypherWebhookInDB

__all__ = ["router"]

router = APIRouter()


@router.get("/webhooks/", response_model=List[BlockCypherWebhookInDB])
async def debug_get():
    return await BlockCypherWebhookCRUD.find_many({})


@router.get("/eth/")
async def debug_get():
    return await SimbaWrapper().issue_tokens(
        "0xbeb3ec5bce587420c00ec547ca2dd5626f497b73",
        100000,
        "manual-test"
    )


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
