from Application.Database.models import Products, ProductImages, Tags
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import and_


class ProductRepositories:
    
    @staticmethod
    async def Load_Product(db: AsyncSession, product_id: int):
        query = select(Products).options(
            joinedload(Products.images).load_only(ProductImages.url)
        ).options(
            joinedload(Products.tags).load_only(Tags.id)
        ).where(Products.id == product_id)

        result = await db.execute(query)

        return result.unique().scalar_one_or_none()

    @staticmethod
    async def Load_Lux_Products(db: AsyncSession, limit: int, offset: int):
        query = select(
            Products.id, Products.name,
            Products.price, Products.discounted_price,
            ProductImages.url
        ).outerjoin(ProductImages, and_(
                ProductImages.product_id == Products.id,
                ProductImages.is_main.is_(True)
        )).where(
            Products.lux == True
        ).limit(limit = limit + 1).offset(limit * offset)

        result = await db.execute(query)
        lux_products = result.all()
        
        has_next = len(lux_products) > limit
        if has_next:
            lux_products = lux_products[:-1]

        return (lux_products, has_next)
    

    @staticmethod
    async def Load_New_Products(db: AsyncSession, limit: int, offset: int):
        query = select(
            Products.id, Products.name,
            Products.price, Products.discounted_price,
            ProductImages.url
        ).outerjoin(ProductImages, and_(
                ProductImages.product_id == Products.id,
                ProductImages.is_main.is_(True)
        )).where(
            Products.new == True
        ).limit(limit = limit + 1).offset(limit * offset)

        result = await db.execute(query)
        new_products = result.all()

        has_next = len(new_products) > limit
        if has_next:
            new_products = new_products[:-1]

        return (new_products, has_next)
    
    @staticmethod
    async def Load_discounted_Products(db: AsyncSession, limit: int, offset: int):
        query = select(
            Products.id, Products.name,
            Products.price, Products.discounted_price,
            ProductImages.url
        ).outerjoin(ProductImages, and_(
            ProductImages.is_main.is_(True),
            ProductImages.product_id == Products.id   
        )).where(
            Products.discounted_price > 0
        ).limit(limit = limit + 1).offset(limit * offset)

        result = await db.execute(query)
        discounted_products = result.all()
        
        has_next = len(discounted_products) > limit
        if has_next:
            discounted_products = discounted_products[:-1]

        return (discounted_products, has_next)