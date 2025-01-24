from fastapi import Request, Response
from datetime import datetime
from hashlib import sha256
from uuid import uuid4
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import UserRepositories
from Application.RedisDB.RedisServices import (
    TokenServices,
    VcodeServices,
    FpasswordForget,
)
from Application.Auth import TokenHandler, BcryptHandler
from Domain.schemas.UserSchemas import (
    VerifyData,
    UserLogin,
    UserPhone,
    ChangePassword,
    UpdateProfile
)
from Domain.Errors.user import PhoneNumberIsExists, UserNotFound, EmptyValues
from Domain.Errors.auth import NoneCode, InvalidCode, InformationMismatch


class UserServices:
    @staticmethod
    async def sing_in(db: AsyncSession, rds: Redis, NewUserData: UserPhone):
        if await UserRepositories.Check_Exists_Phone(db=db, phone=NewUserData.phone):
            raise PhoneNumberIsExists

        code = await VcodeServices.new_verification_code(rds=rds, user=NewUserData)
        return code

    @staticmethod
    async def singin(db: AsyncSession, rds: Redis, response: Response, VerifyData: VerifyData):
        vcode = await VcodeServices.get_verification_code(rds=rds, phone=VerifyData.phone)
        if not vcode:
            raise NoneCode

        hashed_code = sha256(VerifyData.code.encode("utf-8")).hexdigest()
        if hashed_code != vcode:
            raise InvalidCode

        await VcodeServices.delete_verification_code(rds=rds, phone=VerifyData.phone)

        new_user = await UserRepositories.Create_User(
            db=db, 
            UserPhone=VerifyData.phone, 
            UserPassword=BcryptHandler.Hash(VerifyData.password)
        )
        if new_user:
            payload = {"id": str(new_user)}
            access_token = TokenHandler.New_Access_Token(payload=payload)
            refresh_token = TokenHandler.New_Refresh_Token(payload=payload)

            response.set_cookie(
                key="AccessToken",
                value=access_token,
                httponly=True,
                samesite="Strict",
            )
            response.set_cookie(
                key="RefreshToken",
                value=refresh_token,
                httponly=True,
                samesite="Strict",
            )

            return "welcome"

    @staticmethod
    async def login(db: AsyncSession, response: Response, UserData: UserLogin):
        user = await UserRepositories.Login(db=db, phone=UserData.phone)
        if not user or not BcryptHandler.check(password=UserData.password, hashed_password=user[1]):
            raise InformationMismatch

        payload = {"id": str(user[0])}
        access_token = TokenHandler.New_Access_Token(payload=payload)
        refresh_token = TokenHandler.New_Refresh_Token(payload=payload)

        response.set_cookie(
            key="AccessToken",
            value=access_token,
            httponly=True,
            samesite="Strict",
        )
        response.set_cookie(
            key="RefreshToken",
            value=refresh_token,
            httponly=True,
            samesite="Strict",
        )
        return "welcome"

    @staticmethod
    async def forget_password(db: AsyncSession, phone: UserPhone, rds: Redis):
        if not await UserRepositories.Check_Exists_Phone(db=db, phone=phone.phone):
            raise UserNotFound

        code = await FpasswordForget.new_verification_code(rds=rds, phone=phone.phone)
        return code  # send via SMS

    @staticmethod
    async def change_password(db: AsyncSession, UserData: ChangePassword, rds: Redis):
        code = await FpasswordForget.get_forget_code(rds=rds, phone=UserData.phone)
        if not code:
            raise NoneCode

        hashed_code = sha256(UserData.code.encode("utf-8")).hexdigest()
        if code != hashed_code:
            raise InvalidCode

        await FpasswordForget.delete_forget_code(rds=rds, phone=UserData.phone)

        user = await UserRepositories.Get_User_By_Phone(db=db, phone=UserData.phone)
        if user:
            user.password = BcryptHandler.Hash(password=UserData.password)
            password_changed_at = datetime.utcnow()
            user.last_password_change = password_changed_at

            await FpasswordForget.password_changed_at(
                rds=rds, user_id=user.id, time=password_changed_at
            )
            return "Your password has been successfully changed"

    @staticmethod
    async def update_profile(db: AsyncSession, profile: UpdateProfile, user_id: uuid4):
        info = profile.dict(exclude_unset=True)
        if not info:
            raise EmptyValues

        update = await UserRepositories.update(db=db, user_id=user_id, values=info)
        if update:
            return "Your profile has been successfully updated"

    @staticmethod
    async def get_me(db: AsyncSession, user_id: uuid4):
        user = await UserRepositories.Get_User_By_ID(db=db, user_id=user_id)
        if user:
            return {
                "phone": user[0],
                "fullname": user[1],
                "email": user[2],
            }

    @staticmethod
    async def logout(rds: Redis, request: Request, response: Response):
        refresh_token = request.cookies.get("RefreshToken")
        if refresh_token:
            expiry = TokenHandler.get_token_exp_as_secounds(token=refresh_token)
            is_blocked = await TokenServices.is_token_blocked(token=refresh_token, rds=rds)

            if expiry and not is_blocked:
                await TokenServices.block_token(token=refresh_token, expiry=expiry, rds=rds)

        response.delete_cookie(key="AccessToken")
        response.delete_cookie(key="RefreshToken")
        return {"message": "Logged out successfully"}
