from datetime import datetime
from http import HTTPStatus
from urllib.parse import urlencode, urljoin

from fastapi import APIRouter, HTTPException, Depends, Body, Path

from api.dependencies import get_user
from config import HOST_URL
from core.mechanics.referrals import ReferralMechanics
from database.crud import UserCRUD
from schemas import (
    UserLogin,
    User,
    UserLoginResponse,
    UserCreationSafe,
    UserUpdateSafe,
    UserChangePassword,
    UserVerifyEmail,
    SuccessResponse,
    UserRecover,
    UserRecoverLink,
    User2faURL,
    User2faConfirm,
    UserReferralURLResponse,
    User2faDelete,
    UserReferralsResponse,
    UserEthereumSignedAddress,
    USER_MODEL_INCLUDE_FIELDS,
    UserBitcoinAddressDelete,
    UserBitcoinAddressInput,
)

__all__ = ["router"]

router = APIRouter()


@router.get("/user/", response_model=User, response_model_include=USER_MODEL_INCLUDE_FIELDS)
async def account_get_user(user: User = Depends(get_user)):
    return user


@router.post(
    "/login/", response_model=UserLoginResponse,
)
async def account_login(data: UserLogin = Body(...),):
    return await UserCRUD.authenticate(data.email, data.password, data.pin_code)


@router.post("/signup/", response_model=SuccessResponse)
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
    url = (
        urljoin(HOST_URL, "register")
        + "?"
        + (urlencode(params) if user.user_eth_addresses != [] else "referral_id=*************")
    )
    return {"URL": url}


@router.get("/2fa/", response_model=User2faURL)
async def account_create_2fa(user: User = Depends(get_user)):
    return await UserCRUD.create_2fa(user)


@router.post("/2fa/")
async def account_confirm_2fa(user: User = Depends(get_user), payload: User2faConfirm = Body(...)):
    return await UserCRUD.confirm_2fa(user, payload)


@router.delete("/2fa/")
async def account_delete_2fa(user: User = Depends(get_user), payload: User2faDelete = Body(...)):
    return await UserCRUD.delete_2fa(user, payload)


@router.get("/referrals/", response_model=UserReferralsResponse)
async def account_referrals_info(user: User = Depends(get_user)):
    referrals = await ReferralMechanics(user).fetch_referrals()
    transactions = []

    return {"referrals": referrals, "transactions": transactions}


@router.post("/eth-address/")
async def account_eth_address_add(data: UserEthereumSignedAddress = Body(...), user: User = Depends(get_user)):
    filtered_addresses = list(filter(lambda o: o.address == data.address, user.user_eth_addresses))

    if filtered_addresses:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "address already exists")

    user.user_eth_addresses.append(data)

    await UserCRUD.update_one(
        {"_id": user.id}, {"user_eth_addresses": [i.dict() for i in user.user_eth_addresses]}
    )

    return True


@router.delete("/eth-address/{address}")
async def account_add_eth_address_delete(address: str = Path(...), user: User = Depends(get_user)):
    filtered_addresses = list(filter(lambda o: o.address != address, user.user_eth_addresses))

    if len(filtered_addresses) == len(user.user_eth_addresses):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Address does not exist")

    await UserCRUD.update_one({"_id": user.id}, {"user_eth_addresses": [i.dict() for i in filtered_addresses]})

    return True


@router.post("/btc-address/")
async def account_add_btc_address(user: User = Depends(get_user), data: UserBitcoinAddressInput = Body(...)):
    if user.two_factor and not await UserCRUD.check_2fa(user_id=user.id, pin_code=data.pin_code):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect pin-code")

    data.created_at = datetime.now()
    filtered_addresses = list(filter(lambda o: o.address == data.address, user.user_btc_addresses))

    if filtered_addresses:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Address already exists")

    user.user_btc_addresses.append(data)

    await UserCRUD.update_one(
        {"_id": user.id},
        {"user_btc_addresses": [i.dict(exclude={"pin_code"}) for i in user.user_btc_addresses]},
    )

    return True


@router.delete("/btc-address/")
async def account_add_btc_address_delete(
    data: UserBitcoinAddressDelete = Body(...), user: User = Depends(get_user)
):
    if user.two_factor and not await UserCRUD.check_2fa(user_id=user.id, pin_code=data.pin_code):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect pin-code")

    filtered_addresses = list(filter(lambda o: o.address != data.address, user.user_btc_addresses))

    if len(filtered_addresses) == len(user.user_btc_addresses):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Address does not exist")

    await UserCRUD.update_one({"_id": user.id}, {"user_btc_addresses": [i.dict() for i in filtered_addresses]})

    return True
