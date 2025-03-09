from sqlalchemy import UUID, and_, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only, selectinload

from Application.Database.models import OrderItems, Orders
from Domain.schemas.order_schemas import NewOrder


async def add_order(db: AsyncSession, user_id: UUID, order: NewOrder):
    new_order = Orders(
        user_id=user_id,
        address_id=order.address_id,
        discount_id=order.discount_id,
        total_price=order.total_price,
    )

    db.add(new_order)
    await db.flush()
    return new_order.id


async def add_order_items(db: AsyncSession, order_items: list) -> None:
    await db.run_sync(
        lambda sync_session: sync_session.bulk_insert_mappings(
            OrderItems, [item.__dict__ for item in order_items]
        )
    )
    return True
