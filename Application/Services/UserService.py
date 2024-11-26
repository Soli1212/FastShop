from fastapi import Request
from fastapi import Response
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from hashlib import sha256
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis

from Application.Database.repositories import UserRepositories
from Application.Database.repositories import VCodeRepositories
from Application.RedisDB.RedisServices import TokenServices
from Application.Auth import AESHandler
from Application.Auth import TokenHandler
from Application.Auth import Authorize

from Domain.schemas.UserSchemas import UserCreate
from Domain.schemas.UserSchemas import VerifyCode
from Domain.schemas.UserSchemas import UserPhone

from Domain.Errors.user import PhoneNumberIsExists
from Domain.Errors.user import EmailIsExists
from Domain.Errors.user import UserNotFound
from Domain.Errors.auth import NoneCode
from Domain.Errors.auth import InvalidCode
from Domain.Errors.auth import NewUserDataNotFound
from Domain.Errors.auth import InformationMismatch


class UserServices:

    @staticmethod
    async def Verify_New_User(db: AsyncSession, response: Response, NewUserData: UserCreate):

        if await UserRepositories.Check_Exists_Phone(db = db, phone = NewUserData.phone):
            raise PhoneNumberIsExists

        if NewUserData.email and await UserRepositories.Check_Exists_Email(db = db, email = NewUserData.email):
            raise EmailIsExists
        
        SendCode = await VCodeRepositories.new_verification_code(db = db, phone = NewUserData.phone)
        
        UserDataToken = AESHandler(salt = SendCode).encrypt(payload = NewUserData.dict())

        response.set_cookie(
            key = "NUinfo",
            value = UserDataToken,
            httponly = True,
            # secure=True,
            samesite="Strict",
            expires = datetime.now(timezone.utc) + timedelta(minutes=3)
        )
         
        # send {SendCode} with sms 

        return SendCode
    
    @staticmethod
    async def Create_New_User(db: AsyncSession, response: Response, request: Request, VerifyData: VerifyCode):

        Vcode = await VCodeRepositories.get_verification_code(db=db, phone = VerifyData.phone)

        if not Vcode: raise NoneCode

        await VCodeRepositories.delete_verification_code(db = db, phone = VerifyData.phone)

        HashedCode = sha256(VerifyData.code.encode('utf-8')).hexdigest()

        if HashedCode != Vcode: raise InvalidCode

        NewUserData = request.cookies.get("NUinfo", None)
        
        if not NewUserData: raise NewUserDataNotFound
        
        response.delete_cookie("NUinfo")

        cipher = AESHandler(salt = VerifyData.code)
        DecryptedNewUserData = cipher.decrypt(encrypted_data=NewUserData)

        if DecryptedNewUserData.get("phone") != VerifyData.phone:
            raise InformationMismatch
        
        if await UserRepositories.Check_Exists_Phone(db = db, phone = VerifyData.phone):
            raise PhoneNumberIsExists

        NewUser = await UserRepositories.Create_User(
            db = db, 
            NewUserData = UserCreate(**DecryptedNewUserData)
        )
        if NewUser:
            payload = {"id": NewUser} 
            response.set_cookie(
                key = "AccessToken",
                value = TokenHandler.New_Access_Token(payload = payload),
                httponly = True,
                # secure=True,
                samesite="Strict",
            )
           
            response.set_cookie(
                key = "RefreshToken",
                value = TokenHandler.New_Refresh_Token(payload = payload),
                httponly = True,
                # secure=True,
                samesite="Strict",
            )
            return "welcome"
        
    
    @staticmethod
    async def LoginRequest(db: AsyncSession, phone: UserPhone):
        if not await UserRepositories.Check_Exists_Phone(db = db, phone = phone.phone):
            raise UserNotFound
        
        code = await VCodeRepositories.new_verification_code(
            db = db, phone = phone.phone
        ) 

        # send {code} with sms

        return code
    

    @staticmethod
    async def Login(db: AsyncSession, response: Response, VerifyData: VerifyCode):
        Vcode = await VCodeRepositories.get_verification_code(db=db, phone = VerifyData.phone)

        if not Vcode: raise NoneCode

        await VCodeRepositories.delete_verification_code(db = db, phone = VerifyData.phone)

        HashedCode = sha256(VerifyData.code.encode('utf-8')).hexdigest()

        if HashedCode != Vcode: raise InvalidCode

        if user_id := await UserRepositories.get_User_ID_By_Phone(db = db, phone = VerifyData.phone):
            
            payload = {"id": user_id} 
            
            response.set_cookie(
                key = "AccessToken",
                value = TokenHandler.New_Access_Token(payload = payload),
                httponly = True,
                # secure=True,
                samesite="Strict",
            )
           
            response.set_cookie(
                key = "RefreshToken",
                value = TokenHandler.New_Refresh_Token(payload = payload),
                httponly = True,
                # secure=True,
                samesite="Strict",
            )
            return "welcome"
        

    @staticmethod
    async def get_me(db: AsyncSession, user_id: int):
        if user := await UserRepositories.Get_User_By_ID(db = db, user_id = user_id):
            return user


        
    @staticmethod
    async def logout(db: AsyncSession, rds: Redis, request: Request, response: Response):
        auth = await Authorize(
            db = db,
            rds = rds,
            request = request,
            response = response 
        )

        refresh_token = request.cookies.get("RefreshToken")

        ex = TokenHandler.get_token_exp_as_secounds(token = refresh_token)
        Isblocked = await TokenServices.is_token_blocked(token = refresh_token, rds = rds)

        if ex and not Isblocked:
            await TokenServices.block_token(token=refresh_token, expiry=ex, rds=rds)

        response.delete_cookie(key = "AccessToken")
        response.delete_cookie(key = "RefreshToken")

        return {"message": "Logged out successfully"}
