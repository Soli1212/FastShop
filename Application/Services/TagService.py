from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.models import Products, product_tags
from Application.Database.repositories import TagRepository
from Domain.Errors.Tag import PageNotFound


async def get_tags(db: AsyncSession):
    tags = await TagRepository.get_tags(db=db)
    return [i["Tags"] for i in tags]


async def get_tag_products(
    db: AsyncSession, filters: dict, tag_id: int, limit: int = 2
):
    filters_list = [product_tags.c.tag_id == tag_id]

    if min_price := filters.get("min_price"):
        filters_list.append(Products.price >= int(min_price))

    if max_price := filters.get("max_price"):
        filters_list.append(
            or_(
                Products.price <= int(max_price),
                Products.discounted_price <= int(max_price),
            )
        )

    if size := filters.get("size"):
        size_list = [int(i) for i in size.split("-")]
        filters_list.append(Products.sizes.overlap(size_list))

    if color := filters.get("color"):
        color_list = color.split("-")
        filters_list.append(Products.colors.overlap(color_list))

    tag_products = await TagRepository.get_tag_products(
        db=db, filters_list=filters_list, limit=limit, page=int(filters.get("page", 0))
    )

    if not tag_products[0]:
        raise PageNotFound

    return {
        "next_page": tag_products[1],
        "products": tag_products[0],
    }
