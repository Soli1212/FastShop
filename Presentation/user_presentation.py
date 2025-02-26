from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Auth import authorize
from Application.Database import get_db
from Application.RedisDB import RedisConnection
from Application.Services import user_service
from Domain.schemas.user_schemas import UpdateProfile, UserPhone, VerifyData

Router = APIRouter()


@Router.post("/authcode", status_code=status.HTTP_202_ACCEPTED)
async def Verify_New_User(
    NewUserData: UserPhone,
    rds: RedisConnection.get_client = Depends(),
):
    return await user_service.send_auth_code(rds=rds, NewUserData=NewUserData)


@Router.post("/singin", status_code=status.HTTP_202_ACCEPTED)
async def LoginRequest(
    UserData: VerifyData,
    response: Response,
    db: AsyncSession = Depends(get_db),
    rds: RedisConnection.get_client = Depends(),
):
    return await user_service.sing_in(
        db=db, rds=rds, VerifyData=UserData, response=response
    )


@Router.patch("/update", status_code=status.HTTP_200_OK)
async def update(
    profile: UpdateProfile,
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await user_service.update_profile(db=db, profile=profile, user_id=auth["id"])


@Router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    response: Response,
    rds: RedisConnection.get_client = Depends(),
):
    return await user_service.logout(rds=rds, request=request, response=response)


@Router.get("/me", status_code=status.HTTP_200_OK)
async def me(
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await user_service.get_me(db=db, user_id=auth["id"])
