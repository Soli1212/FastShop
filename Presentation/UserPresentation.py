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
from Domain.schemas.UserSchemas import UserPhone



Router = APIRouter()


@Router.post("/sing-up", status_code = status.HTTP_202_ACCEPTED)
async def Verify_New_User(

    response: Response,
    NewUserData: UserCreate,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends()

):
    return await UserServices.Verify_New_User(
        db = db, rds = rds, response = response, 
        NewUserData = NewUserData
    )


@Router.post("/singup", status_code = status.HTTP_201_CREATED)
async def Create_New_User(

    request: Request,
    response: Response,
    VerifyData: VerifyCode,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends()

):
    return await UserServices.Create_New_User(
        db = db, rds = rds, request = request, 
        response = response, VerifyData = VerifyData
    )


@Router.post("/sing-in", status_code = status.HTTP_202_ACCEPTED)
async def LoginRequest(

    phone: UserPhone,
    rds: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),

):
    return await UserServices.LoginRequest(
        db = db, rds = rds, phone = phone
    )


@Router.post("/singin", status_code = status.HTTP_200_OK)
async def Login(

    response: Response,
    VerifyData: VerifyCode,
    rds: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db)

):
    return await UserServices.Login(
        db = db, rds = rds, response = response, 
        VerifyData = VerifyData 
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
    return await UserServices.get_me(db = db, user_id = auth)