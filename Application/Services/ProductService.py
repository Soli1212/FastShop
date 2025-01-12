from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import ProductRepositories
from Domain.Errors.Product import (
    PageNotFound
)


class ProductServices:
    
    @staticmethod
    async def load_product(db: AsyncSession, product_id: int):
        if product := await ProductRepositories.Load_Product(
            db = db, product_id = product_id
        ):
            result = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "discounted_price": product.discounted_price,
                "description": product.description,
                "colors": product.colors,
                "sizes": product.sizes,
                "images": product.images or None,
                "tags": product.tags or None,
                "lux": product.lux,
                "new": product.new,
                "inventory": product.inventory,
                "dimensions": product.dimensions,
            }
            return result
        raise PageNotFound
    
    @staticmethod
    async def lux_products(db: AsyncSession, offset: int, limit: int = 2):
        LuxProducts = await ProductRepositories.Load_Lux_Products(
            db = db, limit = limit, offset = offset
        )

        if not LuxProducts[0]:
            raise PageNotFound

        result = [
            {"id": id, "name": name, "price": price, "discounted_price": discounted_price, "image": images or None}
            for id, name, price, discounted_price, images in LuxProducts[0]
        ]

        return {
            "next_page": LuxProducts[1],
            "products": result
        }

    @staticmethod
    async def new_products(db: AsyncSession, offset: int, limit: int = 2):
        NewProducts = await ProductRepositories.Load_New_Products(
            db = db, limit = limit, offset = offset
        )

        if not NewProducts[0]:
            raise PageNotFound

        result = [
            {"id": id, "name": name, "price": price, "discounted_price": discounted_price, "image": images or None}
            for id, name, price, discounted_price, images in NewProducts[0]
        ]

        return {
            "next_page": NewProducts[1],
            "products": result
        }
    
    @staticmethod
    async def discounted_products(db: AsyncSession, offset: int, limit: int = 2):
        DiscountedProducts = await ProductRepositories.Load_discounted_Products(
            db = db, limit = limit, offset = offset
        )

        if not DiscountedProducts[0]:
            raise PageNotFound

        result = [
            {"id": id, "name": name, "price": price, "discounted_price": discounted_price, "image": images or None}
            for id, name, price, discounted_price, images in DiscountedProducts[0]
        ]

        return {
            "next_page": DiscountedProducts[1],
            "products": result
        }