from uuid import UUID

from sqlalchemy import delete, exists, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Application.Database.models import Addresses
from Domain.schemas.address_schemas import NewAddress


async def get_address_count(db: AsyncSession, user_id: str):
    query = select(func.count(Addresses.id)).where(Addresses.user_id == user_id)
    result = await db.execute(query)
    return result.scalar()


async def add_new_address(db: AsyncSession, new_address: NewAddress, user_id: str):
    address = Addresses(user_id=user_id, **new_address.dict(exclude_unset=True))
    db.add(address)
    return True


async def delete_address(db: AsyncSession, address_id: int, user_id: str):
    query = (
        delete(Addresses)
        .where(Addresses.id == address_id, Addresses.user_id == user_id)
        .returning(Addresses.id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_address(db: AsyncSession, address_id: int, user_id: str):
    query = select(Addresses).where(
        Addresses.id == address_id, Addresses.user_id == user_id
    )
    result = await db.execute(query)
    return result.scalars().first()


async def get_my_addresses(db: AsyncSession, user_id: str):
    query = select(Addresses).where(Addresses.user_id == user_id)
    result = await db.execute(query)
    return result.mappings().all()


async def address_exists(db: AsyncSession, address_id: int, user_id: UUID) -> bool:
    query = select(
        exists().where(Addresses.id == address_id, Addresses.user_id == user_id)
    )
    result = await db.scalar(query)
    return result
