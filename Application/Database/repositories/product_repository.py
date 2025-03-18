from sqlalchemy import and_, case, exists, or_, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only, selectinload

from Application.Database.models import (
    Colors,
    ProductImages,
    ProductInventory,
    Products,
    Tags,
)


async def get_product_details(db: AsyncSession, product_id: int):
    query = (
        select(Products)
        .options(
            joinedload(Products.inventories).load_only(
                ProductInventory.size,
                ProductInventory.color_id,
                ProductInventory.inventory,
            ),
            joinedload(Products.tags).load_only(Tags.id, Tags.name),
            joinedload(Products.images)
            .load_only(ProductImages.url, ProductImages.color_id)
            .joinedload(ProductImages.color)
            .load_only(Colors.name, Colors.hex_code),
        )
        .where(Products.id == product_id)
    )

    result = await db.execute(query)
    product = result.scalars().first()
    return product


async def filter_products(db: AsyncSession, limit: int, offset: int, filter):
    query = (
        select(
            Products.id,
            Products.name,
            Products.price,
            Products.discounted_price,
            Products.inventory,
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
    products = result.mappings().all()

    has_next = len(products) > limit
    if has_next:
        products = products[:limit]

    return products, has_next


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
                ProductInventory.color_id,
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
    selected_color: int,
    selected_size: int,
    required_quantity: int,
) -> bool:
    query = select(
        exists().where(
            ProductInventory.product_id == product_id,
            ProductInventory.color_id == selected_color,
            ProductInventory.size == selected_size,
            ProductInventory.inventory >= required_quantity,
        )
    )
    result = await db.execute(query)
    return result.scalar()


async def update_inventory(
    db: AsyncSession,
    product_updates: list[tuple[int, str | None, str | None, int]],  # پشتیبانی از NULL
) -> None:

    update_conditions = []
    where_conditions = []

    for pid, color_id, size, qty in product_updates:
        color_clause = (
            ProductInventory.color == None
            if color_id is None
            else ProductInventory.color_id == color_id
        )

        size_clause = (
            ProductInventory.size == None
            if size is None
            else ProductInventory.size == size
        )

        condition = and_(ProductInventory.product_id == pid, color_clause, size_clause)

        update_conditions.append((condition, ProductInventory.inventory - qty))

        where_conditions.append(condition)

    stmt = (
        update(ProductInventory)
        .values(inventory=case(*update_conditions, else_=ProductInventory.inventory))
        .where(or_(*where_conditions))
        .where(ProductInventory.inventory >= 0)
    )

    await db.execute(stmt)
    return True
