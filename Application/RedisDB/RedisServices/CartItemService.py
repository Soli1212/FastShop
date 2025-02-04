from json import dumps, loads
from uuid import UUID

from aioredis import Redis

from Domain.Errors.Cart import ProductNotFound
from Domain.schemas.Cart import CartItem, DeleteItem


async def add_or_update_cart(rds: Redis, item: CartItem, user_id: UUID):
    """Add or update an item in the user's cart."""
    key = f"cart:{user_id}"
    field = f"{item.product_id}:{item.color}:{item.size}"
    existing_data = await rds.hget(key, field)

    if existing_data:
        existing_item = loads(existing_data)
        existing_item["quantity"] = item.quantity
        await rds.hset(key, field, dumps(existing_item))
        return "The quantity of the product in your cart has been updated."
    else:
        new_item = {
            "product_id": str(item.product_id),
            "quantity": item.quantity,
            "color": item.color,
            "size": item.size,
        }
        await rds.hset(key, field, dumps(new_item))

    ttl = await rds.ttl(key)
    if ttl == -1 or ttl == -2:
        await rds.expire(key, 86400)  # Set expiration to 24 hours

    return "The product has been added to your cart."


async def remove_cart_item(rds: Redis, user_id: UUID, item: DeleteItem):
    """Remove an item from the user's cart."""
    key = f"cart:{user_id}"
    field = f"{item.product_id}:{item.color}:{item.size}"
    existing_data = await rds.hget(key, field)

    if not existing_data:
        raise ProductNotFound

    await rds.hdel(key, field)
    return "Product removed from cart."


async def get_cart_items(rds: Redis, user_id: UUID):
    key = f"cart:{user_id}"
    cart_items = await rds.hgetall(key)
    if not cart_items:
        return {}
    return [loads(value) for _, value in cart_items.items()]
