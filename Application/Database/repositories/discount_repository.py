from sqlalchemy import and_, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from Application.Database.models import Discounts


async def get_discount(db: AsyncSession, code: str):
    query = select(Discounts).where(Discounts.code == code)
    result = await db.execute(query)
    return result.scalars().first()
