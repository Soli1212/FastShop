from fastapi import Request, Response, Depends

from Application.RedisDB.RedisServices import TokenServices
from Application.RedisDB import RedisConnection
from .JwtHandler import TokenHandler

from Domain.Errors.auth import LoginAgain


async def Authorize(
        
        request: Request, 
        response: Response, 
        redis: RedisConnection.get_client = None,

    ) -> int:
    
    AccessToken = request.cookies.get("AccessToken", None)
   
    if not AccessToken: raise LoginAgain
   
    if VerifyAccessToken := TokenHandler.Verify_Access_Token(token = AccessToken):
        
        return VerifyAccessToken["id"]
    
    #--------------------------------------------------------------------------------------------------

    RefreshToken = request.cookies.get("RefreshToken", None)
    
    if not RefreshToken: raise LoginAgain
    
    rds: RedisConnection.client = redis if redis else await RedisConnection.get_client()
    
    if await TokenServices.is_token_blocked(token = RefreshToken, rds = rds):
        raise LoginAgain

    VerifyRefreshToken = TokenHandler.Verify_Refresh_Token(token = RefreshToken)

    if not VerifyRefreshToken: raise LoginAgain

    NewAccessToken = TokenHandler.New_Access_Token(payload = {"id": VerifyRefreshToken["id"]})

    response.set_cookie(
        key = "AccessToken",
        value = NewAccessToken,
        httponly = True,
        # secure=True,
        samesite="Strict",
    )
        
    return VerifyRefreshToken["id"]