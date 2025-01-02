from Application.Database.models import Tags, Products, ProductImages
from Application.Database.models import product_tags

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy import and_


class TagRepositories:
    
    @staticmethod
    async def Get_Tags(db: AsyncSession):
        query = select(Tags).filter(Tags.parent_id == None).options(
            joinedload(Tags.children).load_only(Tags.id, Tags.name)
        )
        result = await db.execute(query)
        return result.unique().scalars().all()
    

    @staticmethod
    async def Get_Tag_Products(db: AsyncSession, tag_id: int, filters: dict, limit: int):
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

        base_query = (
            select(
                Products.id,
                Products.name,
                Products.price,
                ProductImages.url
            )
            .join(product_tags, product_tags.c.product_id == Products.id)
            .outerjoin(ProductImages, and_(
                ProductImages.product_id == Products.id,
                ProductImages.is_main.is_(True)
            ))
            .group_by(Products.id, ProductImages.url)
            .where(*filters_list)
            .limit(limit)
            .offset(offset)
        )

        total_count_query = (
            select(func.count(Products.id))
            .join(product_tags, product_tags.c.product_id == Products.id)
            .where(*filters_list)
        )

        result = await db.execute(base_query)
        data = result.fetchall()

        total_count_result = await db.execute(total_count_query)
        total_count = total_count_result.scalar_one()

        return (data, total_count)
