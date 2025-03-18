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
        selected_color=item.color_id,
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
    formatted_cart = []
    total_cart = total_discount = 0

    for item in cart_items:
        product = product_map.get(int(item["product_id"]))
        if not product:
            continue

        original = product["price"]
        discounted = product.get("discounted_price")
        qty = item["quantity"]

        final = discounted or original
        item_discount = (original - final) * qty

        formatted_cart.append(
            {
                "product_id": product["id"],
                "name": product["name"],
                "quantity": qty,
                "price": original,
                "discounted_price": discounted or 0,
                "total_price": final * qty,
                "color_id": item.get("color_id"),
                "size": item.get("size"),
            }
        )

        total_cart += final * qty
        total_discount += item_discount

    return {
        "cart_items": formatted_cart,
        "total_cart": total_cart,
        "total_discount": total_discount,
    }
