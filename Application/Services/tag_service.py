from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.models import Products, product_tags
from Application.Database.repositories import tag_repository
from Domain.Errors.tag import PageNotFound


async def get_tags(db: AsyncSession):
    tags = await tag_repository.get_tags(db=db)
    return [i["Tags"] for i in tags]


async def get_tag_products(
    db: AsyncSession,
    tag_id: int,
    min_price: Optional[int],
    max_price: Optional[int],
    size: Optional[str],
    color: Optional[str],
    order_by: str,
    page: int,
    limit: int,
):
    filters = {
        "min_price": min_price,
        "max_price": max_price,
        "size": size,
        "color": color,
    }

    products_tag = await tag_repository.get_tag_products(
        db=db,
        tag_id=tag_id,
        filters=filters,
        order_by=order_by,
        page=page,
        limit=limit,
    )

    return {"next_page": products_tag[1], "products": products_tag[0]}
