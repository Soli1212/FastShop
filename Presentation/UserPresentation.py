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

from Domain.schemas.UserSchemas import VerifyData
from Domain.schemas.UserSchemas import UserLogin
from Domain.schemas.UserSchemas import UserPhone
from Domain.schemas.UserSchemas import ChangePassword
from Domain.schemas.UserSchemas import UpdateProfile



Router = APIRouter()


@Router.post("/sing-up", status_code = status.HTTP_202_ACCEPTED)
async def Verify_New_User(

    response: Response,
    NewUserData: UserPhone,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends()

):
    return await UserServices.sing_in(
        db = db, rds = rds,
        NewUserData = NewUserData
    )


@Router.post("/singup", status_code = status.HTTP_201_CREATED)
async def Create_New_User(
    response: Response,
    VerifyData: VerifyData,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends()

):
    return await UserServices.singin(
        db = db, rds = rds, response = response, VerifyData = VerifyData
    )


@Router.post("/singin", status_code = status.HTTP_202_ACCEPTED)
async def LoginRequest(

    UserData: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),

):
    return await UserServices.login(
        db = db, UserData = UserData, response = response
    )


@Router.post("/forget-pass", status_code = status.HTTP_202_ACCEPTED)
async def ForgetPassword(

    phone: UserPhone,
    rds: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),

):
    return await UserServices.forget_password(
        db = db, phone = phone, rds = rds
    )

@Router.post("/change-pass", status_code = status.HTTP_200_OK)
async def ForgetPassword(

    UserData: ChangePassword,
    rds: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),

):
    return await UserServices.change_password(
        db = db, UserData = UserData, rds = rds
    )

    
@Router.patch("/update", status_code = status.HTTP_200_OK)
async def update(
    profile: UpdateProfile,
    auth: Authorize = Depends()
    
):
    return await UserServices.update_profile(
        db = auth["db"],
        profile = profile,
        user_id = auth["id"]
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
):
    return await UserServices.get_me(db = auth["db"], user_id = auth["id"])