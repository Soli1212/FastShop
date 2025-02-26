from sqlalchemy import and_, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only, selectinload

from Application.Database.models import ProductImages, ProductInventory, Products, Tags


async def get_product_details(db: AsyncSession, product_id: int):
    query = (
        select(Products)
        .options(joinedload(Products.images).load_only(ProductImages.url))
        .options(joinedload(Products.tags).load_only(Tags.id, Tags.name))
        .where(Products.id == product_id)
    )
    result = await db.execute(query)
    return result.unique().mappings().first()


async def filter_products(db: AsyncSession, limit: int, offset: int, filter):
    query = (
        select(
            Products.id,
            Products.name,
            Products.price,
            Products.discounted_price,
            ProductImages.url,
        )
        .outerjoin(
            ProductImages,
            and_(
                ProductImages.product_id == Products.id,
                ProductImages.is_main.is_(True),
            ),
        )
        .where(filter)
        .limit(limit + 1)
        .order_by(Products.created_at.desc(), Products.id.desc())
        .offset(limit * offset)
    )
    result = await db.execute(query)
    lux_products = result.mappings().all()

    has_next = len(lux_products) > limit
    if has_next:
        lux_products = lux_products[:-1]

    return lux_products, has_next


async def get_products_by_ids(db: AsyncSession, product_list: list[int]):
    query = (
        select(
            Products.id,
            Products.name,
            Products.price,
            Products.discounted_price,
            ProductImages.url,
        )
        .outerjoin(
            ProductImages,
            and_(
                ProductImages.product_id == Products.id,
                ProductImages.is_main.is_(True),
            ),
        )
        .where(Products.id.in_(product_list))
    )
    result = await db.execute(query)
    return result.mappings().all()


async def get_products_variants_by_ids(db: AsyncSession, products_ids: list[int]):

    query = (
        select(Products)
        .options(
            load_only(
                Products.id, Products.name, Products.price, Products.discounted_price
            )
        )
        .options(
            selectinload(Products.inventories).load_only(
                ProductInventory.size,
                ProductInventory.color,
                ProductInventory.inventory,
            )
        )
        .where(Products.id.in_(products_ids))
    )

    result = await db.execute(query)
    return result.scalars().all()


async def check_variant_availability(
    db: AsyncSession,
    product_id: int,
    selected_color: str,
    selected_size: int,
    required_quantity: int,
) -> bool:
    query = select(
        exists().where(
            ProductInventory.product_id == product_id,
            ProductInventory.color == selected_color,
            ProductInventory.size == selected_size,
            ProductInventory.inventory >= required_quantity,
        )
    )
    result = await db.execute(query)
    return result.scalar()
