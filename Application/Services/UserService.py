# UserServices.py

from fastapi import Request
from fastapi import Response
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from hashlib import sha256
from sqlalchemy.ext.asyncio import AsyncSession
from Application.Database.repositories import UserRepositories
from Application.Database.repositories import VCodeRepositories
from Application.Auth.AesHandler import AESHandler
from Application.Auth.JwtHandler import TokenHandler

from Domain.schemas.UserSchemas import UserCreate
from Domain.schemas.UserSchemas import VerifyCode

from Domain.Errors.user import PhoneNumberIsExists
from Domain.Errors.user import EmailIsExists
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
        if not Vcode:
            raise NoneCode

        await VCodeRepositories.delete_verification_code(db = db, phone = VerifyData.phone)

        HashCode = sha256(VerifyData.code.encode('utf-8')).hexdigest()

        if HashCode != Vcode:
            raise InvalidCode

        NewUserData = request.cookies.get("NUinfo", None)
        if not NewUserData:
            raise NewUserDataNotFound
        
        response.delete_cookie("NUinfo")

        cipher = AESHandler(salt=VerifyData.code)
        DecryptedNewUserData = cipher.decrypt(encrypted_data=NewUserData)

        if DecryptedNewUserData.get("phone") != VerifyData.phone:
            raise InformationMismatch
        
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

