from datetime import datetime
from hashlib import sha256
from uuid import uuid4

from aioredis import Redis
from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import UserRepository
from Application.RedisDB.RedisServices import ForgetPassword, TokenService, VcodeService
from Application.Auth import BcryptHandler, JwtHandler
from Domain.Errors.auth import InformationMismatch, InvalidCode, NoneCode
from Domain.Errors.user import EmptyValues, PhoneNumberIsExists, UserNotFound
from Domain.schemas.UserSchemas import (
    ChangePassword,
    UpdateProfile,
    UserLogin,
    UserPhone,
    VerifyData,
)
from utils import delete_cookie, set_cookie


async def sing_up(db: AsyncSession, rds: Redis, NewUserData: UserPhone):
    if await UserRepository.check_exists_phone(db=db, phone=NewUserData.phone):
        raise PhoneNumberIsExists

    code = await VcodeService.new_verification_code(rds=rds, user=NewUserData)
    return code  # send code via SMS


async def singup(
    db: AsyncSession, rds: Redis, response: Response, VerifyData: VerifyData
):
    vcode = await VcodeService.get_verification_code(rds=rds, phone=VerifyData.phone)
    if not vcode:
        raise NoneCode

    hashed_code = sha256(VerifyData.code.encode("utf-8")).hexdigest()
    if hashed_code != vcode:
        raise InvalidCode

    await VcodeService.delete_verification_code(rds=rds, phone=VerifyData.phone)

    new_user = await UserRepository.create_user(
        db=db,
        user_phone=VerifyData.phone,
        user_password=BcryptHandler(VerifyData.password).hash_password(),
    )
    if new_user:
        payload = {"id": str(new_user)}
        access_token = JwtHandler.new_access_token(payload=payload)
        refresh_token = JwtHandler.new_refresh_token(payload=payload)

        set_cookie(response=response, key="AccessToken", value=access_token)
        set_cookie(response=response, key="RefreshToken", value=refresh_token)

        return "welcome"


async def login(db: AsyncSession, response: Response, UserData: UserLogin):
    user = await UserRepository.login(db=db, phone=UserData.phone)
    if not user or not BcryptHandler(password=UserData.password).verify_password(
        hashed_password=user.get("password")
    ):
        raise InformationMismatch

    payload = {"id": str(user.get("id"))}
    access_token = JwtHandler.new_access_token(payload=payload)
    refresh_token = JwtHandler.new_refresh_token(payload=payload)

    set_cookie(response=response, key="AccessToken", value=access_token)
    set_cookie(response=response, key="RefreshToken", value=refresh_token)

    return "welcome"


async def forget_password(db: AsyncSession, phone: UserPhone, rds: Redis):
    if not await UserRepository.check_exists_phone(db=db, phone=phone.phone):
        raise UserNotFound

    code = await ForgetPassword.new_verification_code(rds=rds, phone=phone.phone)
    return code  # send via SMS


async def change_password(db: AsyncSession, UserData: ChangePassword, rds: Redis):
    code = await ForgetPassword.get_forget_code(rds=rds, phone=UserData.phone)
    if not code:
        raise NoneCode

    hashed_code = sha256(UserData.code.encode("utf-8")).hexdigest()
    if code != hashed_code:
        raise InvalidCode

    await ForgetPassword.delete_forget_code(rds=rds, phone=UserData.phone)

    user = await UserRepository.get_user_by_phone(db=db, phone=UserData.phone)
    if user:
        user.password = BcryptHandler(password=UserData.password).hash_password()
        password_changed_at = datetime.utcnow()
        user.last_password_change = password_changed_at

        await ForgetPassword.password_changed_at(
            rds=rds, user_id=user.id, time=password_changed_at
        )
        return "Your password has been successfully changed"


async def update_profile(db: AsyncSession, profile: UpdateProfile, user_id: uuid4):
    info = profile.dict(exclude_unset=True)
    if not info:
        raise EmptyValues

    update = await UserRepository.update_profile(db=db, user_id=user_id, values=info)
    if update:
        return "Your profile has been successfully updated"


async def get_me(db: AsyncSession, user_id: uuid4):
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
    return "Logged out successfully"
