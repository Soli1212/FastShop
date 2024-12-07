from fastapi import Request
from fastapi import Response
from fastapi import Depends
from fastapi import APIRouter
from fastapi import status

from Application.Database import get_db
from Application.RedisDB import RedisConnection
from Application.Services import UserServices

from Application.Auth import Authorize

from sqlalchemy.ext.asyncio import AsyncSession

from Domain.schemas.UserSchemas import UserCreate
from Domain.schemas.UserSchemas import VerifyCode
from Domain.schemas.UserSchemas import UserLogin
from Domain.schemas.UserSchemas import UserPhone
from Domain.schemas.UserSchemas import ChangePassword



Router = APIRouter()


@Router.post("/sing-UP", status_code = status.HTTP_202_ACCEPTED)
async def Verify_New_User(

    response: Response,
    NewUserData: UserCreate,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends()

):
    return await UserServices.sing_in(
        db = db, rds = rds, response = response, 
        NewUserData = NewUserData
    )


@Router.post("/singUP", status_code = status.HTTP_201_CREATED)
async def Create_New_User(

    request: Request,
    response: Response,
    VerifyData: VerifyCode,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends()

):
    return await UserServices.singin(
        db = db, rds = rds, request = request, 
        response = response, VerifyData = VerifyData
    )


@Router.post("/singIN", status_code = status.HTTP_202_ACCEPTED)
async def LoginRequest(

    UserData: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),

):
    return await UserServices.login(
        db = db, UserData = UserData, response = response
    )


@Router.post("/forget-Pass", status_code = status.HTTP_202_ACCEPTED)
async def ForgetPassword(

    phone: UserPhone,
    rds: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),

):
    return await UserServices.forget_password(
        db = db, phone = phone, rds = rds
    )

@Router.post("/change-Pass", status_code = status.HTTP_200_OK)
async def ForgetPassword(

    UserData: ChangePassword,
    rds: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),

):
    return await UserServices.change_password(
        db = db, UserData = UserData, rds = rds
    )

    

@Router.get("/logout", status_code = status.HTTP_200_OK)
async def logout(

    request: Request,
    response: Response,
    rds: RedisConnection.get_client = Depends(),

):
    return await UserServices.logout(
        rds = rds, request = request, 
        response = response
    )


@Router.get("/me", status_code = status.HTTP_200_OK)
async def me(
    auth: Authorize = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await UserServices.get_me(db = auth["db"], user_id = auth["id"])