from uuid import UUID

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import ProductRepository
from Application.RedisDB.RedisServices import CartItemService
from Domain.Errors.Cart import NonExistent
from Domain.schemas.Cart import CartItem, DeleteItem


async def add_to_cart(db: AsyncSession, rds: Redis, item: CartItem, user_id: int):
    product_inventory = await ProductRepository.variant_exists(
        db=db,
        product_id=item.product_id,
        selected_color=item.color,
        selected_size=item.size,
        required_quantity=item.quantity,
    )

    if not product_inventory:
        raise NonExistent

    return await CartItemService.add_or_update_cart(rds=rds, item=item, user_id=user_id)


async def delete_product(rds: Redis, user_id: UUID, item: DeleteItem):
    return await CartItemService.remove_cart_item(rds=rds, user_id=user_id, item=item)


async def get_cart(db: AsyncSession, rds: Redis, user_id: UUID):
    cart_items = await CartItemService.get_cart_items(rds=rds, user_id=user_id)
    if not cart_items:
        return "Your cart is empty"

    product_ids = list({int(item["product_id"]) for item in cart_items})
    products = await ProductRepository.get_products_list(
        db=db, product_list=product_ids
    )
    product_map = {p["id"]: p for p in products}

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

        finall_price = discounted_price if discounted_price else original_price
        item_discount = (original_price - finall_price) * quantity
        total_discount += item_discount

        finall_price *= quantity

        formatted_item = {
            "product_id": product_id,
            "name": product["name"],
            "quantity": quantity,
            "price": original_price,
            "discounted_price": discounted_price or 0,
            "total_price": finall_price,
            "color": item.get("color"),
            "size": item.get("size"),
        }
        formatted_cart.append(formatted_item)
        total_cart += finall_price

    return {
        "cart_items": formatted_cart,
        "total_cart": total_cart,
        "total_discount": total_discount,
    }
