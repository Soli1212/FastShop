from hashlib import sha256
from random import randint

from aioredis import Redis

from Domain.Errors.Vcode import SendedCode
from Domain.schemas.UserSchemas import UserPhone


async def exists_verification_code(rds: Redis, phone: str) -> bool:
    key = f"Signup_code:{phone}"
    result = await rds.exists(key)
    return result == 1


async def new_verification_code(rds: Redis, user: UserPhone, expiry: int = 120):
    if await exists_verification_code(rds=rds, phone=user.phone):
        raise SendedCode

    randcode = str(randint(10000, 99999)).encode("utf-8")
    key = f"Signup_code:{user.phone}"
    value = sha256(randcode).hexdigest()

    await rds.set(key, value, ex=expiry)

    return randcode.decode("utf-8")


async def get_verification_code(rds: Redis, phone: str):
    key = f"Signup_code:{phone}"
    code = await rds.get(key)
    return code


async def delete_verification_code(rds: Redis, phone: str):
    key = f"Signup_code:{phone}"
    result = await rds.delete(key)
    return result == 1
