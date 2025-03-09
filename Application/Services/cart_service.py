from uuid import UUID

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import product_repository
from Application.RedisDB.RedisServices import cart_item_service
from Domain.Errors.cart import NonExistent
from Domain.schemas.cart_schemas import CartItem, DeleteItem
from utils import json_response


async def add_to_cart(db: AsyncSession, rds: Redis, item: CartItem, user_id: UUID):
    product_inventory = await product_repository.check_variant_availability(
        db=db,
        product_id=item.product_id,
        selected_color=item.color,
        selected_size=item.size,
        required_quantity=item.quantity,
    )

    if not product_inventory:
        raise NonExistent

    if await cart_item_service.add_or_update_cart(rds=rds, item=item, user_id=user_id):
        return await get_cart(db=db, rds=rds, user_id=user_id)


async def delete_product(db: AsyncSession, rds: Redis, user_id: UUID, item: DeleteItem):
    if await cart_item_service.remove_cart_item(rds=rds, user_id=user_id, item=item):
        return await get_cart(db=db, rds=rds, user_id=user_id)


async def get_cart(db: AsyncSession, rds: Redis, user_id: UUID) -> dict:
    cart_items = await cart_item_service.get_cart_items(rds=rds, user_id=user_id)
    if not cart_items:
        return json_response(msg="Your cart is empty")

    product_ids = {int(i["product_id"]) for i in cart_items}

    products = await product_repository.get_products_by_ids(
        db=db, product_list=product_ids
    )

    product_map = {p["id"]: p for p in products}

    return calculate_final_price(cart_items=cart_items, product_map=product_map)


def calculate_final_price(cart_items: list, product_map: dict):
    total_cart = 0
    total_discount = 0
    formatted_cart = []

    for item in cart_items:
        product_id = int(item["product_id"])
        product = product_map.get(product_id)

        if not product:
            continue

        original_price = product.get("price")
        discounted_price = product.get("discounted_price")
        quantity = item["quantity"]

        final_price = discounted_price if discounted_price else original_price
        item_discount = (original_price - final_price) * quantity
        total_discount += item_discount

        final_price *= quantity

        formatted_item = {
            "product_id": product_id,
            "name": product["name"],
            "quantity": quantity,
            "price": original_price,
            "discounted_price": discounted_price or 0,
            "total_price": final_price,
            "color": item.get("color"),
            "size": item.get("size"),
        }
        formatted_cart.append(formatted_item)
        total_cart += final_price

    return {
        "cart_items": formatted_cart,
        "total_cart": total_cart,
        "total_discount": total_discount,
    }
