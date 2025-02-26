from asyncio import gather
from datetime import datetime

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import (
    address_repository,
    discount_repository,
    product_repository,
)
from Application.RedisDB.RedisServices import cart_item_service
from Domain.Errors.address import AddressNotFound
from Domain.Errors.discount import (
    DiscountLimit,
    InvalidDiscountCode,
    UnauthorizeDiscount,
)
from Domain.Errors.order import (
    InsufficientInventory,
    ProductNotAvalible,
    ProductNotFound,
)
from Domain.schemas.order_schemas import Order
from utils import json_response

from .cart_service import calculate_final_price


def check_discount_code(dicount, total_price: int, user_id: int):
    if total_price < dicount.min_order_value:
        raise DiscountLimit(limit=str(dicount.min_order_value))

    current_time = datetime.utcnow()

    if current_time < dicount.start_date or current_time > dicount.end_date:
        raise InvalidDiscountCode

    if dicount.user_id and user_id != dicount.user_id:
        raise InvalidDiscountCode

    discounted_total_price = int(
        total_price - ((total_price / 100) * dicount.discount_percentage)
    )

    total_discount = total_price - discounted_total_price

    return (discounted_total_price, total_discount)


def validate_cart_inventory(products_map: dict, user_cart: list) -> None:
    for item in user_cart:
        product_id = int(item["product_id"])
        size = item.get("size")
        color = item.get("color")
        quantity = item["quantity"]

        product = products_map.get(product_id)

        if not product:
            raise ProductNotFound

        variant_key = (size, color)
        variants = {(inv.size, inv.color): inv for inv in product["inventories"]}
        variant = variants.get(variant_key)

        if not variant:
            raise ProductNotAvalible
        if variant.inventory < quantity:
            raise InsufficientInventory

    return True


async def prepare_order(user_id: int, order: Order, db: AsyncSession, rds: Redis):
    UserCart = await cart_item_service.get_cart_items(rds=rds, user_id=user_id)
    if not UserCart:
        return json_response(msg="Your cart is empty")

    UserCartProducts = {int(i["product_id"]) for i in UserCart}

    Products_Detaild, valid_address = await gather(
        product_repository.get_products_variants_by_ids(
            db=db, products_ids=UserCartProducts
        ),
        address_repository.address_exists(
            db=db, address_id=order.address_id, user_id=user_id
        ),
    )

    if not valid_address:
        raise AddressNotFound

    Products_Detaild_Mapp = {i.id: i.__dict__ for i in Products_Detaild}

    validate_cart_inventory(products_map=Products_Detaild_Mapp, user_cart=UserCart)

    factor = calculate_final_price(
        cart_items=UserCart, product_map=Products_Detaild_Mapp
    )
    factor.update({"address_id": order.address_id})

    if order.discount_code:
        if factor.get("total_discount"):
            raise UnauthorizeDiscount

        discount = await discount_repository.get_discount(
            db=db, code=order.discount_code
        )
        if not discount:
            raise InvalidDiscountCode

        discounted = check_discount_code(
            dicount=discount, total_price=factor.get("total_cart"), user_id=user_id
        )
        factor.update(
            {
                "total_cart": discounted[0],
                "total_discount": discounted[1],
                "discount_code": order.discount_code,
            }
        )

    return factor
