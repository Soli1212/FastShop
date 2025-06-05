from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.models import Products
from Application.Database.repositories import product_repository
from Domain.Errors.product import PageNotFound


async def load_product(db: AsyncSession, product_id: int):
    """Getting the specifications of a product"""
    if product := await product_repository.get_product_details(
        db=db, product_id=product_id
    ):
        result = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "dimensions": product.dimensions,
            "price": product.price,
            "discounted_price": product.discounted_price,
            "new": product.new,
            "lux": product.lux,
            "best_selling": product.best_selling,
            "inventory": product.inventory,
            "tags": product.tags,
            "sizes": product.sizes,
            "images": product.images,
            "inventories": product.inventories,
        }
        return result
    raise PageNotFound


class ProductFilterType(Enum):
    LUX = "lux"
    NEW = "new"
    DISCOUNTED = "discounted"
    best_selling = "best-selling"


async def get_filtered_products(
    db: AsyncSession, filter_type: ProductFilterType, offset: int, limit: int = 2
):
    """Get filtered products"""
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


async def get_random_products(
    db: AsyncSession,
    filter_type: str,
):
    """Get random products"""

    filter_mapping = {
        "new": Products.new == True,
        "lux": Products.lux == True,
        "best_selling": Products.best_selling == True,
        "discounted": Products.discounted_price > 0,
    }

    random_products = await product_repository.get_random_products(
        db=db, filter_condition=filter_mapping.get(filter_type, Products.lux == True)
    )

    return random_products


async def search_products(
    db: AsyncSession,
    offset: int, 
    prompt: str,
    limit: int = 2,
    
):
    """search products"""
    
    products = await product_repository.search_products(
        db = db, limit = limit, offset = offset, prompt=prompt
    )

    if not products[0]:
        raise PageNotFound

    return {"next_page": products[1], "products": products[0]}
