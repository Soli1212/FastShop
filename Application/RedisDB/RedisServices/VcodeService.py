from aioredis import Redis
from random import randint
from hashlib import sha256

from Domain.Errors.Vcode import SendedCode

class VcodeServices:

    @staticmethod
    async def new_verification_code(rds: Redis, phone: str, expiry: int = 120):
        if await VcodeServices.exists_verification_code(rds=rds, phone=phone):
            raise SendedCode
        
        randcode = str(randint(10000, 99999)).encode('utf-8')
        key = f"verify_code:{phone}"
        value = sha256(randcode).hexdigest()

        await rds.set(key, value, ex=expiry)
        
        return randcode.decode('utf-8')

    @staticmethod
    async def exists_verification_code(rds: Redis, phone: str) -> bool:
        key = f"verify_code:{phone}"
        result = await rds.exists(key)
        return result == 1

    @staticmethod
    async def get_verification_code(rds: Redis, phone: str):
        key = f"verify_code:{phone}"
        result = await rds.get(key)
        return result

    @staticmethod
    async def delete_verification_code(rds: Redis, phone: str):

        key = f"verify_code:{phone}"
        result = await rds.delete(key)
        return result == 1
