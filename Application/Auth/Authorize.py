from fastapi import Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Application.Database.connection import get_db

from Application.Database.repositories import UserRepositories
from Application.RedisDB.RedisServices import TokenServices
from Application.RedisDB import get_redis_client
from .JwtHandler import TokenHandler

from Domain.Errors.auth import LoginAgain
from Domain.Errors.auth import UserNotFound


async def Authorize(request: Request, 
        response: Response, 
        db: AsyncSession = Depends(get_db), 
        rds: get_redis_client = Depends()
    ) -> int:
    
    AccessToken = request.cookies.get("AccessToken", None)
   
    if not AccessToken: raise LoginAgain
   
    if VerifyAccessToken := TokenHandler.Verify_Access_Token(token = AccessToken):

        if not await UserRepositories.Check_Exists_ID(db = db, user_id = VerifyAccessToken["id"]): 
            raise UserNotFound
        
        return {"user_id": VerifyAccessToken["id"], "db": db}
    
    #--------------------------------------------------------------------------------------------------

    RefreshToken = request.cookies.get("RefreshToken", None)
    
    if not RefreshToken: raise LoginAgain

    if await TokenServices.is_token_blocked(token = RefreshToken, rds = rds):
        raise LoginAgain

    VerifyRefreshToken = TokenHandler.Verify_Refresh_Token(token = RefreshToken)

    if not VerifyRefreshToken: raise LoginAgain

    NewAccessToken = TokenHandler.New_Access_Token(payload = {"id": VerifyRefreshToken["id"]})

    if not await UserRepositories.Check_Exists_ID(db = db, user_id = VerifyRefreshToken["id"]): 
        raise UserNotFound

    response.set_cookie(
        key = "AccessToken",
        value = NewAccessToken,
        httponly = True,
        # secure=True,
        samesite="Strict",
    )
        
    return {"user_id": VerifyRefreshToken["id"], "db": db}