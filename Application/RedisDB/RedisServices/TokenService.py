from aioredis import Redis


class TokenServices:

    @staticmethod
    async def block_token(token: str, expiry: int, rds: Redis):
        key = f"blocked_token:{token}"
        await rds.set(key, "blocked", ex = expiry)

    @staticmethod
    async def is_token_blocked(token: str, rds: Redis) -> bool:
        key = f"blocked_token:{token}"
        result = await rds.exists(key)
        return result == 1