from datetime import datetime, timedelta
from os import getenv

from dotenv import load_dotenv
from jwt import decode, encode

from Domain.Errors.auth import LoginAgain

load_dotenv()
ACCESS_TOKEN_KEY = getenv("ACCESS_TOKEN_KEY")
REFRESH_TOKEN_KEY = getenv("REFRESH_TOKEN_KEY")


def new_access_token(payload: dict, exp: int = 15) -> str:
    """Generate a new access token with expiration time."""
    payload["exp"] = datetime.utcnow() + timedelta(minutes=exp)
    return encode(payload=payload, key=ACCESS_TOKEN_KEY, algorithm="HS256")


def new_refresh_token(payload: dict, exp: int = 7) -> str:
    """Generate a new refresh token with expiration time."""
    payload["exp"] = datetime.utcnow() + timedelta(days=exp)
    return encode(payload=payload, key=REFRESH_TOKEN_KEY, algorithm="HS256")


def verify_access_token(token: str) -> dict:
    """Verify and decode the access token."""
    try:
        return decode(jwt=token, key=ACCESS_TOKEN_KEY, algorithms=["HS256"])
    except Exception:
        return False


def verify_refresh_token(token: str) -> dict:
    """Verify and decode the refresh token."""
    try:
        return decode(jwt=token, key=REFRESH_TOKEN_KEY, algorithms=["HS256"])
    except Exception:
        raise LoginAgain


def get_token_exp_as_seconds(token: str) -> int:
    verified_token = verify_refresh_token(token)
    exp_time = datetime.utcfromtimestamp(verified_token["exp"])
    remaining_seconds = (exp_time - datetime.utcnow()).total_seconds()
    return int(remaining_seconds) if remaining_seconds > 0 else None
