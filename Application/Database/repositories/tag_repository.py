from typing import Tuple

from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only, selectinload

from Application.Database.models import (
    ProductImages,
    Products,
    Tags,
    product_colors,
    product_tags,
)


async def get_tags(db: AsyncSession):
    query = (
        select(Tags)
        .where(Tags.parent_id == None)
        .options(joinedload(Tags.children).load_only(Tags.id, Tags.name))
    )
    result = await db.execute(query)
    return result.unique().mappings().all()


async def get_tag_products(
    db: AsyncSession,
    tag_id: int,
    filters: dict,
    order_by: str,
    page: int,
    limit: int,
) -> Tuple[list, bool]:

    query = (
        select(
            Products.id,
            Products.name,
            Products.price,
            Products.discounted_price,
            Products.inventory,
            ProductImages.url,
        )
        .join(product_tags, product_tags.c.product_id == Products.id)
        .outerjoin(
            ProductImages,
            and_(
                ProductImages.product_id == Products.id,
                ProductImages.is_main.is_(True),
            ),
        )
        .where(product_tags.c.tag_id == tag_id)
    )

    if min_price := filters.get("min_price"):
        query = query.where(Products.price >= min_price)

    if max_price := filters.get("max_price"):
        query = query.where(
            or_(Products.discounted_price <= max_price, Products.price <= max_price)
        )

    if size := filters.get("size"):
        size_list = [int(s) for s in size.split("-")]
        query = query.where(Products.sizes.overlap(size_list))

    if color := filters.get("color"):
        color_ids = [int(c) for c in color.split("-")]
        query = (
            query.join(product_colors, product_colors.c.product_id == Products.id)
            .where(product_colors.c.color_id.in_(color_ids))
            .group_by(Products.id, ProductImages.url)
            .having(func.count(product_colors.c.color_id) >= len(color_ids))
        )

    order_mapping = {
        "new": Products.created_at.desc(),
        "sale": Products.best_selling.desc(),
        "mxp": Products.price.desc(),
        "mnp": Products.price.asc(),
        "deafult": Products.id.desc(),
    }

    query = query.order_by(order_mapping.get(order_by, Products.id.desc()))

    query = query.limit(limit + 1).offset(page * limit)

    result = await db.execute(query)
    products = result.mappings().all()

    has_next = len(products) > limit
    return products[:limit], has_next


async def get_random_products_tag(db: AsyncSession, tag_id: int):
    subquery = (
        select(
            Products.id,
            Products.name,
            Products.price,
            Products.discounted_price,
            ProductImages.url.label("main_image"),
            func.random().label("rand"),
        )
        .join(product_tags, product_tags.c.product_id == Products.id)
        .join(Tags, Tags.id == product_tags.c.tag_id)
        .outerjoin(
            ProductImages,
            (ProductImages.product_id == Products.id) & (ProductImages.is_main == True),
        )
        .where(Tags.id == tag_id)
        .order_by(func.random())
        .limit(20)
        .alias("subq")
    )

    query = (
        select(
            subquery.c.id,
            subquery.c.name,
            subquery.c.price,
            subquery.c.discounted_price,
            subquery.c.main_image,
        )
        .distinct(subquery.c.id)
        .order_by(subquery.c.id, subquery.c.rand)
        .limit(10)
    )

    result = await db.execute(query)
    return result.mappings().all()
