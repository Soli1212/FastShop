from datetime import datetime
from hashlib import sha256
from uuid import UUID

from aioredis import Redis
from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Auth import JwtHandler
from Application.Database.repositories import UserRepository
from Application.RedisDB.RedisServices import TokenService, VcodeService
from Domain.Errors.auth import InvalidCode, NoneCode
from Domain.Errors.user import EmptyValues
from Domain.schemas.UserSchemas import UpdateProfile, UserPhone, VerifyData
from utils import delete_cookie, json_response, set_cookie


async def send_auth_code(rds: Redis, NewUserData: UserPhone):
    code = await VcodeService.new_verification_code(rds=rds, user=NewUserData)
    return json_response(msg=code, key="code")  # send code via SMS


async def sing_in(
    db: AsyncSession, rds: Redis, response: Response, VerifyData: VerifyData
):
    vcode = await VcodeService.get_verification_code(rds=rds, phone=VerifyData.phone)
    if not vcode:
        raise NoneCode

    hashed_code = sha256(VerifyData.code.encode("utf-8")).hexdigest()
    if hashed_code != vcode:
        raise InvalidCode

    await VcodeService.delete_verification_code(rds=rds, phone=VerifyData.phone)

    if user := await UserRepository.login(db=db, phone=VerifyData.phone):
        payload = {"id": str(user.get("id"))}
    else:
        if user := await UserRepository.create_user(db=db, user_phone=VerifyData.phone):
            payload = {"id": str(user)}

    access_token = JwtHandler.new_access_token(payload=payload)
    refresh_token = JwtHandler.new_refresh_token(payload=payload)

    set_cookie(response=response, key="AccessToken", value=access_token)
    set_cookie(response=response, key="RefreshToken", value=refresh_token)

    return json_response(msg="welcome")


async def update_profile(db: AsyncSession, profile: UpdateProfile, user_id: UUID):
    info = profile.dict(exclude_unset=True)
    if not info:
        raise EmptyValues

    update = await UserRepository.update_profile(db=db, user_id=user_id, values=info)
    if update:
        return await get_me(db=db, user_id=user_id)


async def get_me(db: AsyncSession, user_id: UUID):
    if user := await UserRepository.get_user_by_id(db=db, user_id=user_id):
        return user


async def logout(rds: Redis, request: Request, response: Response):
    refresh_token = request.cookies.get("RefreshToken")
    if refresh_token:
        expiry = JwtHandler.get_token_exp_as_seconds(token=refresh_token)
        is_blocked = await TokenService.is_token_blocked(token=refresh_token, rds=rds)

        if expiry and not is_blocked:
            await TokenService.block_token(token=refresh_token, expiry=expiry, rds=rds)

    delete_cookie(response=response, key="AccessToken")
    delete_cookie(response=response, key="RefreshToken")

    return json_response(msg="Logged out successfully")
