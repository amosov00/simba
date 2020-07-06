from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request, Response
from urllib.parse import urlencode, urljoin

from core.mechanics.crypto import BitcoinWrapper
from core.mechanics.referrals import ReferralMechanics
from config import HOST_URL
from api.dependencies import get_user
from database.crud import UserCRUD, ReferralCRUD
from schemas import (
    UserLogin,
    User,
    UserLoginResponse,
    UserCreationSafe,
    UserUpdateSafe,
    UserChangePassword,
    UserVerifyEmail,
    UserCreationSafeResponse,
    UserRecover,
    UserRecoverLink,
    User2faURL,
    User2faConfirm,
    UserReferralURLResponse,
    User2faDelete,
    UserReferralsResponse,
    USER_MODEL_INCLUDE_FIELDS,
)

__all__ = ["router"]

router = APIRouter()


@router.get(
    "/user/",
    response_model=User,
    # TODO update
    response_model_include=USER_MODEL_INCLUDE_FIELDS,
)
async def account_get_user(user: User = Depends(get_user)):
    return user


@router.post(
    "/login/", response_model=UserLoginResponse,
)
async def account_login(data: UserLogin = Body(...),):
    return await UserCRUD.authenticate(data.email, data.password, data.pin_code)


@router.post("/signup/", response_model=UserCreationSafeResponse)
async def account_signup(data: UserCreationSafe = Body(...)):
    return await UserCRUD.create_safe(data)


@router.put("/user/")
async def account_update_user(user: User = Depends(get_user), payload: UserUpdateSafe = Body(...)):
    return await UserCRUD.update_safe(user, payload) if payload.dict(exclude_unset=True) else {}


@router.post("/change_password/")
async def account_change_password(user: User = Depends(get_user), payload: UserChangePassword = Body(...)):
    return await UserCRUD.change_password(user, payload)


@router.post("/verify/", response_model=UserLoginResponse)
async def account_verify_email(data: UserVerifyEmail = Body(...)):
    return await UserCRUD.verify_email(data.email, data.verification_code)


@router.post("/recover/")
async def account_recover_send(data: UserRecover = Body(...)):
    return await UserCRUD.recover_send(data)


@router.put("/recover/")
async def account_recover(data: UserRecoverLink = Body(...)):
    return await UserCRUD.recover(data)


@router.get("/referral_link/", response_model=UserReferralURLResponse)
async def account_get_referral_link(user: User = Depends(get_user)):
    params = {"referral_id": user.id}
    url = urljoin(HOST_URL, "register") + "?" + urlencode(params)
    return {"URL": url}


@router.get("/2fa/", response_model=User2faURL)
async def account_create_2fa(user: User = Depends(get_user)):
    return await UserCRUD.create_2fa(user)


@router.post("/2fa/")
async def account_confirm_2fa(user: User = Depends(get_user), payload: User2faConfirm = Body(...)):
    return await UserCRUD.confirm_2fa(user, payload)


# TODO deprecated, delete after 07/09/20
# @router.get("/btc-address/")
# async def account_btc_address(user: User = Depends(get_user)):
#     if not user.btc_address:
#         address = await BitcoinWrapper().create_wallet_address(user)
#     else:
#         address = user.btc_address
#
#     return {"address": address}


@router.delete("/2fa/")
async def account_delete_2fa(user: User = Depends(get_user), payload: User2faDelete = Body(...)):
    return await UserCRUD.delete_2fa(user, payload)


@router.get("/referrals/", response_model=UserReferralsResponse)
async def account_referrals_info(user: User = Depends(get_user)):
    ref_obj = ReferralMechanics(user)
    referrals = await ref_obj.fetch_referrals()
    transactions = []

    return {"referrals": referrals, "transactions": transactions}
