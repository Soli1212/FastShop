from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from datetime import datetime
from hashlib import sha256
from uuid import uuid4
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from asyncio import sleep

from Application.Database.repositories import UserRepositories
from Application.RedisDB.RedisServices import (
    TokenServices,
    VcodeServices,
    FpasswordForget,
)
from Application.Auth import AESHandler, TokenHandler, BcryptHandler
from Domain.schemas.UserSchemas import (
    UserCreate,
    VerifyCode,
    UserLogin,
    UserPhone,
    ChangePassword,
    UpdateProfile
)
from Domain.Errors.user import PhoneNumberIsExists, EmailIsExists, UserNotFound
from Domain.Errors.auth import (
    NoneCode,
    InvalidCode,
    InformationMismatch,
)


class UserServices:
    @staticmethod
    async def sing_in(db: AsyncSession, rds: Redis, NewUserData: UserCreate):

        if await UserRepositories.Check_Exists_Phone(db=db, phone=NewUserData.phone):
            raise PhoneNumberIsExists

        hashed_password = BcryptHandler.Hash(password=NewUserData.password)
        NewUserData.password = hashed_password

        Code = await VcodeServices.new_verification_code(rds=rds, user = NewUserData)

        return Code

    @staticmethod
    async def singin(
        db: AsyncSession, rds: Redis, request: Request, response: Response, VerifyData: VerifyCode
    ):
        Vcode = await VcodeServices.get_verification_code(rds=rds, phone=VerifyData.phone)
        
        if not Vcode:
            raise NoneCode

        HashedCode = sha256(VerifyData.code.encode("utf-8")).hexdigest()

        if HashedCode != Vcode.get("code"):
            raise InvalidCode

        await VcodeServices.delete_verification_code(rds=rds, phone=VerifyData.phone)

        if NewUser := await UserRepositories.Create_User(
            db=db, NewUserData = UserCreate(phone = VerifyData.phone, password = Vcode.get("password"))
        ):
            payload = {"id": str(NewUser)}
            AccessToken = TokenHandler.New_Access_Token(payload=payload)
            RefreshToken = TokenHandler.New_Refresh_Token(payload=payload)

            response.set_cookie(
                key="AccessToken",
                value = AccessToken,
                httponly=True,
                # secure=True,
                samesite="Strict",
            )

            response.set_cookie(
                key="RefreshToken",
                value = RefreshToken,
                httponly=True,
                # secure=True,
                samesite="Strict",
            )

            return "welcome"

    @staticmethod
    async def login(db: AsyncSession, response: Response, UserData: UserLogin):
        if user := await UserRepositories.Login(db=db, phone=UserData.phone):

            if not BcryptHandler.check(password=UserData.password, hashed_password = user[1]): 
                raise InformationMismatch

            payload = {"id": str(user[0])}

            Access_TOKEN = TokenHandler.New_Access_Token(payload=payload)
            Refresh_TOKEN = TokenHandler.New_Refresh_Token(payload=payload)

            response.set_cookie(
                key="AccessToken",
                value=Access_TOKEN,
                httponly=True,
                # secure=True,
                samesite="Strict",
            )
            response.set_cookie(
                key="RefreshToken",
                value=Refresh_TOKEN,
                httponly=True,
                # secure=True,
                samesite="Strict",
            )
            return "welcome"
        else:
            raise UserNotFound

    @staticmethod
    async def forget_password(db: AsyncSession, phone: UserPhone, rds: Redis):
        if not await UserRepositories.Check_Exists_Phone(db=db, phone=phone.phone):
            raise UserNotFound

        code = await FpasswordForget.new_verification_code(rds=rds, phone=phone.phone)

        # send code with SMS
        return code

    @staticmethod
    async def change_password(db: AsyncSession, UserData: ChangePassword, rds: Redis):
        if code := await FpasswordForget.get_forget_code(rds=rds, phone=UserData.phone):
            HashedCode = sha256(UserData.code.encode("utf-8")).hexdigest()

            if code != HashedCode:
                raise InvalidCode

            await FpasswordForget.delete_forget_code(rds=rds, phone=UserData.phone)

            if User := await UserRepositories.Get_User_By_Phone(db=db, phone=UserData.phone):
                User.password = BcryptHandler.Hash(password = UserData.password)
                password_changed_at = datetime.utcnow()
                
                print(password_changed_at)

                User.last_password_change = password_changed_at
                await FpasswordForget.password_changed_at(
                    rds=rds, user_id=User.id, time=password_changed_at
                )

                return "Your password has been successfully changed"
        else:
            raise NoneCode
        
    @staticmethod    
    async def update_profile(db: AsyncSession, profile: UpdateProfile, user_id: uuid4):
        update = await UserRepositories.update(
            db = db, user_id = user_id, 
            values = profile.dict()
        )
        if update: return "Your profile has been successfully updated"

    @staticmethod
    async def get_me(db: AsyncSession, user_id: uuid4):
        if user := await UserRepositories.Get_User_By_ID(db=db, user_id = user_id):
            return {
                "id": user.id,
                "phone": user.phone,
                "fullname": user.fullname,
                "email": user.email,
            }

    @staticmethod
    async def logout(rds: Redis, request: Request, response: Response):
        refresh_token = request.cookies.get("RefreshToken", None)

        if refresh_token:
            ex = TokenHandler.get_token_exp_as_secounds(token=refresh_token)
            Isblocked = await TokenServices.is_token_blocked(token=refresh_token, rds=rds)

            if ex and not Isblocked:
                await TokenServices.block_token(token=refresh_token, expiry=ex, rds=rds)

        response.delete_cookie(key="AccessToken")
        response.delete_cookie(key="RefreshToken")

        return {"message": "Logged out successfully"}
