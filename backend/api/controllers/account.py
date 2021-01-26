from datetime import datetime
from http import HTTPStatus
from urllib.parse import urlencode, urljoin

from fastapi import APIRouter, HTTPException, Depends, Body, Path

from api.dependencies import get_user
from config import settings, SST_CONTRACT
from core.integrations.person_verify import PersonVerifyClient
from core.mechanics.referrals import ReferralMechanics
from database.crud import UserCRUD, EthereumTransactionCRUD, UserAddressesArchiveCRUD
from schemas import (
    UserLogin,
    User,
    UserLoginResponse,
    UserCreationSafe,
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
    UserAddressesArchive,
    UserKYCAccessTokenResponse
)

__all__ = ["router"]

router = APIRouter()


@router.get("/user/", response_model=User, response_model_include=USER_MODEL_INCLUDE_FIELDS)
async def account_get_user(user: User = Depends(get_user)):
    return user


@router.post(
    "/login/",
    response_model=UserLoginResponse,
)
async def account_login(
    data: UserLogin = Body(...),
):
    return await UserCRUD.authenticate(data.email, data.password, data.pin_code)


@router.post("/signup/", response_model=SuccessResponse)
async def account_signup(data: UserCreationSafe = Body(...)):
    return await UserCRUD.create_safe(data)


# Deprecated at 17/08/20, uncomment if necessary
# @router.put("/user/")
# async def account_update_user(user: User = Depends(get_user), payload: UserUpdateSafe = Body(...)):
#     return await UserCRUD.update_safe(user, payload) if payload.dict(exclude_unset=True) else {}


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
    if user.user_eth_addresses:
        params = {"referral_id": user.id}
    else:
        params = {"referral_id": "*************"}

    return {
        "url": urljoin(settings.common.host_url, "register") + "?" + urlencode(params),
        "partner_code": str(user.id),
    }


@router.get("/2fa/", response_model=User2faURL)
async def account_create_2fa(user: User = Depends(get_user)):
    return await UserCRUD.create_2fa(user)


@router.post("/2fa/")
async def account_confirm_2fa(user: User = Depends(get_user), payload: User2faConfirm = Body(...)):
    return await UserCRUD.confirm_2fa(user, payload)


@router.delete("/2fa/")
async def account_delete_2fa(user: User = Depends(get_user), payload: User2faDelete = Body(...)):
    return await UserCRUD.delete_2fa(user, payload)


@router.get("/kyc/token/", response_model=UserKYCAccessTokenResponse)
async def account_get_kyc_token(user: User = Depends(get_user)):
    return {
        "token": await PersonVerifyClient.get_access_token(str(user.id))
    }


@router.get("/referrals/", response_model=UserReferralsResponse)
async def account_referrals_info(user: User = Depends(get_user)):
    instance = ReferralMechanics(user)
    referrals = await instance.fetch_referrals_top_to_bottom()

    transactions = await EthereumTransactionCRUD.find_many(
        {
            "contract": SST_CONTRACT.title,
            "user_id": user.id,
        }
    )

    transactions = await instance.fetch_sst_tx_info_for_user(transactions)

    return {"referrals": referrals, "transactions": transactions}


@router.post("/eth-address/")
async def account_eth_address_add(data: UserEthereumSignedAddress = Body(...), user: User = Depends(get_user)):
    filtered_addresses = list(filter(lambda o: o.address.lower() == data.address.lower(), user.user_eth_addresses))

    if filtered_addresses:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "address already exists")

    user.user_eth_addresses.append(data)

    await UserCRUD.update_one({"_id": user.id}, {"user_eth_addresses": [i.dict() for i in user.user_eth_addresses]})

    return True


@router.delete("/eth-address/{address}")
async def account_add_eth_address_delete(address: str = Path(...), user: User = Depends(get_user)):
    addresses_to_save = list(filter(lambda o: o.address.lower() != address.lower(), user.user_eth_addresses))
    if len(addresses_to_save) == len(user.user_eth_addresses):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Address does not exist")

    address_to_delete = list(filter(lambda o: o.address.lower() == address.lower(), user.user_eth_addresses))[0]

    await UserCRUD.update_one({"_id": user.id}, {"user_eth_addresses": [i.dict() for i in addresses_to_save]})
    await UserAddressesArchiveCRUD.insert_one(
        UserAddressesArchive(
            user_id=user.id,
            address=address_to_delete.address,
            signature=address_to_delete.signature,
        ).dict()
    )

    return True


@router.post("/btc-address/")
async def account_add_btc_address(user: User = Depends(get_user), data: UserBitcoinAddressInput = Body(...)):
    if user.two_factor and not await UserCRUD.check_2fa(user_id=user.id, pin_code=data.pin_code):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect pin-code")

    data.created_at = datetime.now()
    filtered_addresses = list(filter(lambda o: o.address.lower() == data.address.lower(), user.user_btc_addresses))

    if filtered_addresses:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Address already exists")

    user.user_btc_addresses.append(data)

    await UserCRUD.update_one(
        {"_id": user.id},
        {"user_btc_addresses": [i.dict(exclude={"pin_code"}) for i in user.user_btc_addresses]},
    )

    return True


@router.delete("/btc-address/")
async def account_add_btc_address_delete(data: UserBitcoinAddressDelete = Body(...), user: User = Depends(get_user)):
    if user.two_factor and not await UserCRUD.check_2fa(user_id=user.id, pin_code=data.pin_code):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect pin-code")

    addresses_to_save = list(filter(lambda o: o.address.lower() != data.address.lower(), user.user_btc_addresses))

    if len(addresses_to_save) == len(user.user_btc_addresses):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Address does not exist")

    address_to_delete = list(filter(lambda o: o.address.lower() == data.address.lower(), user.user_btc_addresses))[0]

    await UserCRUD.update_one({"_id": user.id}, {"user_btc_addresses": [i.dict() for i in addresses_to_save]})
    await UserAddressesArchiveCRUD.insert_one(
        UserAddressesArchive(
            user_id=user.id,
            address=address_to_delete.address,
        ).dict()
    )

    return True
