from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database import get_db
from Application.RedisDB import RedisConnection
from Application.Auth import authorize
from Application.Services import UserService
from Domain.schemas.UserSchemas import (
    ChangePassword,
    UpdateProfile,
    UserLogin,
    UserPhone,
    VerifyData,
)

Router = APIRouter()


@Router.post("/sing-up", status_code=status.HTTP_202_ACCEPTED)
async def Verify_New_User(
    NewUserData: UserPhone,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends(),
):
    return await UserService.sing_up(db=db, rds=rds, NewUserData=NewUserData)


@Router.post("/singup", status_code=status.HTTP_201_CREATED)
async def Create_New_User(
    response: Response,
    VerifyData: VerifyData,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends(),
):
    return await UserService.singup(
        db=db, rds=rds, response=response, VerifyData=VerifyData
    )


@Router.post("/singin", status_code=status.HTTP_202_ACCEPTED)
async def LoginRequest(
    UserData: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.login(db=db, UserData=UserData, response=response)


@Router.post("/forget-pass", status_code=status.HTTP_202_ACCEPTED)
async def ForgetPassword(
    phone: UserPhone,
    rds: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await UserService.forget_password(db=db, phone=phone, rds=rds)


@Router.patch("/change-pass", status_code=status.HTTP_200_OK)
async def ForgetPassword(
    UserData: ChangePassword,
    rds: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await UserService.change_password(db=db, UserData=UserData, rds=rds)


@Router.patch("/update", status_code=status.HTTP_200_OK)
async def update(profile: UpdateProfile, auth: authorize = Depends()):
    return await UserService.update_profile(
        db=auth["db"], profile=profile, user_id=auth["id"]
    )


@Router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    response: Response,
    rds: RedisConnection.get_client = Depends(),
):
    return await UserService.logout(rds=rds, request=request, response=response)


@Router.get("/me", status_code=status.HTTP_200_OK)
async def me(
    auth: authorize = Depends(),
):
    return await UserService.get_me(db=auth["db"], user_id=auth["id"])
