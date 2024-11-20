from jwt import encode, decode
from Domain.Errors.auth import LoginAgain
from datetime import timedelta, datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()
ACCESS_TOKEN_KEY = getenv("ACCESS_TOKEN_KEY")
REFRESH_TOKEN_KEY = getenv("REFRESH_TOKEN_KEY")

class TokenHandler:

    @staticmethod
    def New_Access_Token(payload: dict, exp: int = 20) -> str:
        payload["exp"] = datetime.utcnow() + timedelta(minutes = exp)
        token = encode(payload = payload, key = ACCESS_TOKEN_KEY, algorithm = "HS256")
        return token


    @staticmethod
    def New_Refresh_Token(payload: dict, exp: int = 30) -> str:
        payload["exp"] = datetime.utcnow() + timedelta(days = exp)
        token = encode(payload = payload, key = REFRESH_TOKEN_KEY, algorithm = "HS256")
        return token


    @staticmethod
    def Verify_Access_Token(token: str) -> dict:
        try:
            DecodedToken = decode(jwt = token, key = ACCESS_TOKEN_KEY, algorithms = "HS256")
            return DecodedToken
        except :
            return False

    @staticmethod
    def Verify_Refresh_Token(token: str) -> dict:
        try:
            DecodedToken = decode(jwt = token, key = REFRESH_TOKEN_KEY, algorithms = "HS256")
            return DecodedToken
        except:
            raise LoginAgain