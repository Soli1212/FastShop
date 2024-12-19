from datetime import datetime
from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from Application.Database import get_db
from Application.Database.repositories import UserRepositories
from Application.RedisDB import RedisConnection
from Application.RedisDB.RedisServices import FpasswordForget, TokenServices
from .JwtHandler import TokenHandler

from Domain.Errors.auth import LoginAgain


async def check_iat(
        
    db: AsyncSession,
    rds: RedisConnection.get_client,
    user_id: uuid4,
    jwt_iat: datetime,

) -> bool:
    
    password_changed_at = await FpasswordForget.get_password_changed_at(rds=rds, user_id = user_id)

    if not password_changed_at:
        password_changed_at = str(
            await UserRepositories.Get_User_Last_Password_Change(db=db, user_id=user_id)
        )
        await FpasswordForget.password_changed_at(rds=rds, user_id=user_id, time=password_changed_at)

    password_changed_at_timestamp = (
        datetime.strptime(password_changed_at, "%Y-%m-%d %H:%M:%S.%f")
    ).timestamp()

    return jwt_iat > password_changed_at_timestamp


async def Authorize(
        
    request: Request,
    response: Response,
    redis: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),
    
) -> dict:
    # -------------------------------------------------------------
    AccessToken = request.cookies.get("AccessToken", None)
    RefreshToken = request.cookies.get("RefreshToken", None)

    if await TokenServices.is_token_blocked(token=RefreshToken, rds=redis):
        raise LoginAgain
    # -------------------------------------------------------------

    if not AccessToken:
        raise LoginAgain

    if VerifyAccessToken := TokenHandler.Verify_Access_Token(token=AccessToken):
        if await check_iat(
            db=db, rds=redis, jwt_iat=VerifyAccessToken["iat"], user_id=VerifyAccessToken["id"]
        ):
            return {"id": VerifyAccessToken["id"], "db": db, "rds": redis}

    # --------------------------------------------------------------------------------------------------
    if not RefreshToken:
        raise LoginAgain

    VerifyRefreshToken = TokenHandler.Verify_Refresh_Token(token=RefreshToken)

    if not VerifyRefreshToken:
        raise LoginAgain

    if not await check_iat(
        db=db, rds=redis, jwt_iat=VerifyRefreshToken["iat"], user_id=VerifyRefreshToken["id"]
    ):
        raise LoginAgain

    NewAccessToken = TokenHandler.New_Access_Token(payload = {"id": VerifyRefreshToken["id"]})

    response.set_cookie(
        key="AccessToken",
        value=NewAccessToken,
        httponly=True,
        # secure=True,
        samesite="Strict",
    )

    return {"id": VerifyRefreshToken["id"], "db": db, "rds": redis}
