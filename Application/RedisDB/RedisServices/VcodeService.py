from aioredis import Redis
from random import randint
from hashlib import sha256

from Domain.Errors.Vcode import SendedCode
from Domain.schemas.UserSchemas import UserCreate

class VcodeServices:

    @staticmethod
    async def new_verification_code(rds: Redis, user: UserCreate, expiry: int = 120):
        if await VcodeServices.exists_verification_code(rds=rds, phone=user.phone):
            raise SendedCode
        
        randcode = str(randint(10000, 99999)).encode('utf-8')
        key = f"Singup_code:{user.phone}"
        mapping = {
            "code": sha256(randcode).hexdigest(),
            "password": user.password
        }

        await rds.hmset(key, mapping=mapping)
        await rds.expire(key, expiry)
        
        return randcode.decode('utf-8')

    @staticmethod
    async def exists_verification_code(rds: Redis, phone: str) -> bool:
        key = f"Singup_code:{phone}"
        result = await rds.exists(key)
        return result == 1

    @staticmethod
    async def get_verification_code(rds: Redis, phone: str):
        key = f"Singup_code:{phone}"
        code = (await rds.hmget(name = key, keys = ["code"]))[0]
        password = (await rds.hmget(name = key, keys = "password"))[0]
        if code and password : return {"code": code, "password": password}
        return None
    
    @staticmethod
    async def delete_verification_code(rds: Redis, phone: str):

        key = f"Singup_code:{phone}"
        result = await rds.delete(key)
        return result == 1  
