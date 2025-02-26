from fastapi import Depends, Request, Response

from Application.RedisDB import RedisConnection
from Application.RedisDB.RedisServices import token_service
from Domain.Errors.auth import LoginAgain
from utils import set_cookie

from . import jwt_handler


async def authorize(
    request: Request,
    response: Response,
    redis: RedisConnection.get_client = Depends(),
) -> dict:
    """Authorize user based on access and refresh tokens."""
    access_token = request.cookies.get("AccessToken")
    refresh_token = request.cookies.get("RefreshToken")

    if await token_service.is_token_blocked(token=refresh_token, rds=redis):
        raise LoginAgain

    if not access_token:
        raise LoginAgain

    if verify_access_token := jwt_handler.verify_access_token(token=access_token):
        return {"id": verify_access_token["id"], "rds": redis}

    if not refresh_token:
        raise LoginAgain

    if verify_refresh_token := jwt_handler.verify_refresh_token(token=refresh_token):
        new_access_token = jwt_handler.new_access_token(
            payload={"id": verify_refresh_token["id"]}
        )
        set_cookie(response=response, key="AccessToken", value=new_access_token)

        return {"id": verify_refresh_token["id"], "rds": redis}
    else:
        raise LoginAgain
