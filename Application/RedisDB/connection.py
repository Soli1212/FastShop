import asyncio
import logging
from os import getenv

from aioredis import from_url, Redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379/0")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RedisConnection:
    client: Redis = None
    _lock = asyncio.Lock()

    @classmethod
    async def initialize(cls):
        async with cls._lock:
            if cls.client:
                return True
            try:
                cls.client = await from_url(
                    url=REDIS_URL, max_connections=10, decode_responses=True
                )
                if await cls.client.ping():
                    logger.info("Redis connected successfully")
                else:
                    logger.error("Redis ping failed")
                    raise Exception("Redis ping failed")
            except Exception as e:
                logger.exception("Redis Connection Failed: %s", e)
                cls.client = None
                raise

    @classmethod
    async def get_client(cls) -> Redis:
        if cls.client is None:
            await cls.initialize()
        if cls.client is not None:
            return cls.client
        else:
            raise Exception("Redis client is not available")

    @classmethod
    async def close(cls):
        if cls.client:
            await cls.client.close()
            cls.client = None
