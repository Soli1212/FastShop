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


async def lux_products(db: AsyncSession, offset: int, limit: int = 2):
    lux_products = await product_repository.filter_products(
        db=db, limit=limit, offset=offset, filter=Products.lux == True
    )

    if not lux_products[0]:
        raise PageNotFound

    return {"next_page": lux_products[1], "products": lux_products[0]}


async def new_products(db: AsyncSession, offset: int, limit: int = 2):
    new_products = await product_repository.filter_products(
        db=db, limit=limit, offset=offset, filter=Products.new == True
    )

    if not new_products[0]:
        raise PageNotFound

    return {"next_page": new_products[1], "products": new_products[0]}


async def discounted_products(db: AsyncSession, offset: int, limit: int = 2):
    discounted_products = await product_repository.filter_products(
        db=db, limit=limit, offset=offset, filter=Products.discounted_price > 0
    )

    if not discounted_products[0]:
        raise PageNotFound

    return {"next_page": discounted_products[1], "products": discounted_products[0]}
