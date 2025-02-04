from datetime import datetime
from uuid import UUID

from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database import get_db
from Application.Database.repositories import UserRepository
from Application.RedisDB import RedisConnection
from Application.RedisDB.RedisServices import ForgetPassword, TokenService
from Domain.Errors.auth import LoginAgain
from utils import set_cookie

from . import JwtHandler


async def check_iat(
    db: AsyncSession,
    redis_client: RedisConnection.get_client,
    user_id: UUID,
    jwt_iat: datetime,
) -> bool:
    """Check if the JWT issuance time is valid based on password change time."""
    password_changed_at = await ForgetPassword.get_password_changed_at(
        rds=redis_client, user_id=user_id
    )

    if not password_changed_at:
        if db_time := await UserRepository.get_user_last_password_change(
            db=db, user_id=user_id
        ):
            password_changed_at = str(db_time.get("last_password_change"))
            await ForgetPassword.password_changed_at(
                rds=redis_client, user_id=user_id, time=password_changed_at
            )

    if password_changed_at:
        password_changed_at_timestamp = datetime.strptime(
            password_changed_at, "%Y-%m-%d %H:%M:%S.%f"
        ).timestamp()
        return jwt_iat > password_changed_at_timestamp

    return True


async def authorize(
    request: Request,
    response: Response,
    redis: RedisConnection.get_client = Depends(),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Authorize user based on access and refresh tokens."""
    access_token = request.cookies.get("AccessToken")
    refresh_token = request.cookies.get("RefreshToken")

    if await TokenService.is_token_blocked(token=refresh_token, rds=redis):
        raise LoginAgain

    if not access_token:
        raise LoginAgain

    verify_access_token = JwtHandler.verify_access_token(token=access_token)
    if verify_access_token:
        if await check_iat(
            db=db,
            redis_client=redis,
            jwt_iat=verify_access_token["iat"],
            user_id=verify_access_token["id"],
        ):
            return {"id": verify_access_token["id"], "db": db, "rds": redis}

    if not refresh_token:
        raise LoginAgain

    verify_refresh_token = JwtHandler.verify_refresh_token(token=refresh_token)
    if not verify_refresh_token:
        raise LoginAgain

    if not await check_iat(
        db=db,
        redis_client=redis,
        jwt_iat=verify_refresh_token["iat"],
        user_id=verify_refresh_token["id"],
    ):
        raise LoginAgain

    new_access_token = JwtHandler.new_access_token(
        payload={"id": verify_refresh_token["id"]}
    )
    set_cookie(response=response, key="AccessToken", value=new_access_token)

    return {"id": verify_refresh_token["id"], "db": db, "rds": redis}
