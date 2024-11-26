from fastapi import HTTPException
from aioredis import from_url
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
REDIS_URL = getenv("REDIS_URL")


class RedisConnection:
    _redis_pool = None

    @classmethod
    async def initialize(cls):
        if cls._redis_pool is None:
            try:
                cls._redis_pool = await from_url(
                    REDIS_URL,
                    max_connections=10,
                    decode_responses=True
                )
                if await cls._redis_pool.ping():
                    print("Redis connected successfully")
            except Exception:
                print("Redis Connection Failed")
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to connect to Redis"
                )

    @classmethod
    async def get_client(cls):
        if cls._redis_pool is None:
            await cls.initialize()
        return cls._redis_pool

    @classmethod
    async def close(cls):
        if cls._redis_pool:
            await cls._redis_pool.close()
            cls._redis_pool = None


async def get_redis_client():
    redis = await RedisConnection.get_client()
    if not redis:
        raise HTTPException(
            status_code=500, 
            detail="Redis connection not available"
        )
    return redis
