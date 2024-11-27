from jwt import encode
from jwt import decode

from json import loads
from base64 import b64decode

from datetime import datetime
from datetime import timedelta

from dotenv import load_dotenv
from os import getenv

from Domain.Errors.auth import LoginAgain




load_dotenv()
ACCESS_TOKEN_KEY = getenv("ACCESS_TOKEN_KEY")
REFRESH_TOKEN_KEY = getenv("REFRESH_TOKEN_KEY")

class TokenHandler:

    @staticmethod
    def New_Access_Token(payload: dict, exp: int = 15) -> str:
        payload["exp"] = datetime.utcnow() + timedelta(seconds = exp)
        token = encode(payload = payload, key = ACCESS_TOKEN_KEY, algorithm = "HS256")
        return token


    @staticmethod
    def New_Refresh_Token(payload: dict, exp: int = 7) -> str:
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
        
    @staticmethod
    def get_token_exp_as_secounds(token: str):
        payload = token.split(".")[1]
        payload = b64decode(payload + "==").decode("utf-8")
        payload = loads(payload)
        exp_time = datetime.utcfromtimestamp(payload['exp'])
        current_time = datetime.utcnow()
        remaining_time = exp_time - current_time
        remaining_seconds  = remaining_time.total_seconds()
        if remaining_seconds> 0:
            return int(remaining_seconds)
        else:
            return None
