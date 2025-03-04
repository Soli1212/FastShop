import json
from uuid import UUID

from aioredis import Redis


async def save_temp_order(
    order: dict, user_id: UUID, rds: Redis, exp: int = 100
) -> bool:
    key = f"order:{user_id}"
    order_json = json.dumps(order, ensure_ascii=False)
    await rds.set(key, order_json, ex=exp)
    return True


async def user_temp_order(user_id: UUID, rds: Redis) -> dict:
    key = f"order:{user_id}"
    try:
        order_json = await rds.get(key)
        if order_json:
            return json.loads(order_json)
        return {}
    except Exception as e:
        print(f"Error retrieving temp order: {e}")
        return {}
