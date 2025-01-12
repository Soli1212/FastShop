from Application.Database.models import Tags, Products, ProductImages
from Application.Database.models import product_tags

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy import and_

from typing import Tuple

class TagRepositories:
    
    @staticmethod
    async def Get_Tags(db: AsyncSession):
        query = select(Tags).filter(Tags.parent_id == None).options(
            joinedload(Tags.children).load_only(Tags.id, Tags.name)
        )
        result = await db.execute(query)
        return result.unique().scalars().all()
    
    @staticmethod
    async def Get_Tag_Products(db: AsyncSession, tag_id: int, filters: dict, limit: int) -> Tuple[list, bool]:
        page = int(filters.get("page", 0))
        offset = page * limit

        filters_list = [product_tags.c.tag_id == tag_id]

        if f := filters.get("min_price"):
            filters_list.append(Products.price >= int(f))
        if f := filters.get("max_price"):
            filters_list.append(Products.price <= int(f))
        if f := filters.get("size"):
            size_list = [int(i) for i in f.split("-")]
            filters_list.append(Products.sizes.overlap(size_list))
        if f := filters.get("color"):
            color_list = f.split("-")
            filters_list.append(Products.colors.overlap(color_list))

        query = (
            select(
                Products.id,
                Products.name,
                Products.price,
                Products.discounted_price,
                ProductImages.url
            )
            .join(product_tags, product_tags.c.product_id == Products.id)
            .outerjoin(ProductImages, and_(
                ProductImages.product_id == Products.id,
                ProductImages.is_main.is_(True)
            ))

            .where(*filters_list)
            .limit(limit + 1)
            .offset(offset)
        )

        result = await db.execute(query)
        products = result.all()


        has_next = len(products) > limit
        if has_next:
            products = products[:-1]

        return (products, has_next)
