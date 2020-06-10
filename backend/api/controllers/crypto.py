from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request
import ujson

from api.dependencies import get_user
from core.mechanics import BitcoinWrapper
from schemas import User, EthereumContract
from config import SIMBA_CONTRACT

__all__ = ["router"]

router = APIRouter()


# TODO Temp endpoint. Move to user account
@router.get(
    "/btc/get_address/"
)
async def account_get_user(
        user: User = Depends(get_user)
):
    if not user.btc_address:
        address = await BitcoinWrapper().create_wallet_address(user)
    else:
        address = user.btc_address

    return {"address": address}


@router.get(
    "/eth/contract/",
    dependencies=Depends(get_user),
    response_model=EthereumContract,
    response_model_exclude={"abi_filepath"},
)
async def meta_contract_fetch():
    contract = SIMBA_CONTRACT

    with open(contract.abi_filepath) as f:
        abi = ujson.load(f)
        contract.abi = abi

    return contract

