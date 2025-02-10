from typing import Tuple
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from Application.Database.models import ProductImages, Products, Tags, product_tags


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
    filters_list: list,
    limit: int,
    order_by: str = "new",
    page: int = 0,
) -> Tuple[list, bool]:

    query = (
        select(
            Products.id,
            Products.name,
            Products.price,
            Products.discounted_price,
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
        .where(*filters_list)
        .order_by(Products.created_at.desc(), Products.id.desc())
        .limit(limit + 1)
        .offset(page * limit)
    )

    if order_by == "new":
        query = query.order_by(Products.created_at.desc(), Products.id.desc())

    elif order_by == "sale":
        query = query.order_by(Products.best_selling.desc(), Products.id.desc())

    elif order_by == "mxp":
        query = query.order_by(Products.price.desc())

    elif order_by == "mnp":
        query = query.order_by(Products.price.asc())

    result = await db.execute(query)
    products = result.mappings().all()

    has_next = len(products) > limit
    if has_next:
        products = products[:-1]

    return products, has_next
