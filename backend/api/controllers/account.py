from typing import List
from http import HTTPStatus
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request, Response

from api.dependencies import get_user
from database.crud import UserCRUD
from schemas.user import (
    UserLogin,
    User,
    UserLoginResponse,
    UserCreationSafe,
    UserUpdateSafe,
    UserChangePassword,
    UserVerifyEmail,
    UserVerifyEmailResponse,
    UserCreationSafeResponse,
    UserRecover,
    UserRecoverLink,
    User2faURL,
)

__all__ = ["router"]

router = APIRouter()


@router.post("/recover/")
async def account_recover_send(data: UserRecover = Body(...)):
    return await UserCRUD.recover_send(data)


@router.put("/recover/")
async def account_recover(data: UserRecoverLink = Body(...)):
    return await UserCRUD.recover(data)


@router.post("/login/", response_model=UserLoginResponse, response_model_exclude={"recover_code", "auth_code"})
async def account_login(
        response: Response,
        data: UserLogin = Body(...),
):
    resp = await UserCRUD.authenticate(data.email, data.password, data.pin_code)
    # TODO Make secure cookie token
    response.set_cookie(key="accessToken", value=resp["token"], secure=True, httponly=True)
    return resp


@router.post("/signup/", response_model=UserCreationSafeResponse)
async def account_signup(data: UserCreationSafe = Body(...)):
    return await UserCRUD.create_safe(data)


@router.post("/verify/", response_model=UserLoginResponse)
async def account_verify_email(data: UserVerifyEmail = Body(...)):
    return await UserCRUD.verify_email(data.email, data.verification_code)

# @router.post("/logout/", dependencies=[Depends(get_user)])
# async def account_signup(
#         response: Response,
# ):
#     response.delete_cookie(key="accessToken")
#     return {"success": True}


@router.get("/user/", response_model=User, response_model_exclude={"_id", "recover_code", "auth_code"})
async def account_get_user(user: User = Depends(get_user)):
    return user


@router.put("/user/")
async def account_update_user(user: User = Depends(get_user), payload: UserUpdateSafe = Body(...)):
    resp = await UserCRUD.update_safe(user, payload) if payload.dict(exclude_unset=True) else {}
    return resp


@router.post("/change_password/")
async def account_change_password(user: User = Depends(get_user), payload: UserChangePassword = Body(...)):
    resp = await UserCRUD.change_password(user, payload)
    return resp


@router.get("/create_2fa/", response_model=User2faURL)
async def create_2fa(user: User = Depends(get_user)):
    return await UserCRUD.create_2fa(user)
