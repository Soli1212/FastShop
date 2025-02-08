from fastapi import Depends, Request, Response

from Application.RedisDB import RedisConnection
from Application.RedisDB.RedisServices import TokenService
from Domain.Errors.auth import LoginAgain
from utils import set_cookie

from . import JwtHandler


async def authorize(
    request: Request,
    response: Response,
    redis: RedisConnection.get_client = Depends(),
) -> dict:
    """Authorize user based on access and refresh tokens."""
    access_token = request.cookies.get("AccessToken")
    refresh_token = request.cookies.get("RefreshToken")

    if await TokenService.is_token_blocked(token=refresh_token, rds=redis):
        raise LoginAgain

    if not access_token:
        raise LoginAgain

    if verify_access_token := JwtHandler.verify_access_token(token=access_token):
        return {"id": verify_access_token["id"], "rds": redis}

    if not refresh_token:
        raise LoginAgain

    if verify_refresh_token := JwtHandler.verify_refresh_token(token=refresh_token):
        new_access_token = JwtHandler.new_access_token(
            payload={"id": verify_refresh_token["id"]}
        )
        set_cookie(response=response, key="AccessToken", value=new_access_token)

        return {"id": verify_refresh_token["id"], "rds": redis}
    else:
        raise LoginAgain
