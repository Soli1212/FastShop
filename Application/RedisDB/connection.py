from os import getenv

from aioredis import from_url
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()
REDIS_URL = getenv("REDIS_URL")


class RedisConnection:
    client = None

    @classmethod
    async def initialize(cls):
        if cls.client:
            return True

        try:
            cls.client = await from_url(
                url=REDIS_URL, max_connections=10, decode_responses=True
            )

            if await cls.client.ping():
                print("Redis connected successfully")

        except Exception:
            print("Redis Connection Failed")

    @classmethod
    async def get_client(cls):
        if cls.client is None:
            await cls.initialize()
        if cls.client:
            return cls.client

    @classmethod
    async def close(cls):
        if cls.client:
            await cls.client.close()
            cls.client = None
