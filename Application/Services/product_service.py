from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.models import Products
from Application.Database.repositories import product_repository
from Domain.Errors.product import PageNotFound


async def load_product(db: AsyncSession, product_id: int):
    if product := await product_repository.get_product_details(
        db=db, product_id=product_id
    ):
        return product["Products"]
    raise PageNotFound


class ProductFilterType(Enum):
    LUX = "lux"
    NEW = "new"
    DISCOUNTED = "discounted"
    best_selling = "best-selling"


async def get_filtered_products(
    db: AsyncSession, filter_type: ProductFilterType, offset: int, limit: int = 2
):
    match filter_type:
        case ProductFilterType.LUX:
            filter_condition = Products.lux == True
        case ProductFilterType.NEW:
            filter_condition = Products.new == True
        case ProductFilterType.best_selling:
            filter_condition = Products.best_selling == True
        case ProductFilterType.DISCOUNTED:
            filter_condition = Products.discounted_price > 0
        case _:
            filter_condition = Products.lux == True

    filtered_products = await product_repository.filter_products(
        db=db, limit=limit, offset=offset, filter=filter_condition
    )

    if not filtered_products[0]:
        raise PageNotFound

    return {"next_page": filtered_products[1], "products": filtered_products[0]}
