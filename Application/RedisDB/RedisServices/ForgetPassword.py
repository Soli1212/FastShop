from datetime import datetime
from hashlib import sha256
from random import randint

from aioredis import Redis

from Domain.Errors.Vcode import SendedCode


async def exists_forget_code(rds: Redis, phone: str) -> bool:
    key = f"forget_code:{phone}"
    result = await rds.exists(key)
    return result == 1


async def new_verification_code(rds: Redis, phone: str, expiry: int = 120):
    if await exists_forget_code(rds=rds, phone=phone):
        raise SendedCode

    randcode = str(randint(10000, 99999)).encode("utf-8")
    key = f"forget_code:{phone}"
    value = sha256(randcode).hexdigest()

    await rds.set(key, value, ex=expiry)

    return randcode.decode("utf-8")


async def get_forget_code(rds: Redis, phone: str):
    key = f"forget_code:{phone}"
    result = await rds.get(key)
    return result


async def delete_forget_code(rds: Redis, phone: str):
    key = f"forget_code:{phone}"
    result = await rds.delete(key)
    return result == 1


async def password_changed_at(rds: Redis, user_id: int, time: datetime):
    key = f"password_changed_at:{user_id}"
    await rds.set(key, str(time), ex=86400)


async def get_password_changed_at(rds: Redis, user_id: int):
    key = f"password_changed_at:{user_id}"
    result = await rds.get(key)
    return result
