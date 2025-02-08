from uuid import uuid4

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import load_only
from sqlalchemy.sql import exists

from Application.Database.models import Users


async def create_user(db: AsyncSession, user_phone: str):
    """Add new user"""
    new_user = Users(phone=user_phone)
    db.add(new_user)
    await db.flush()
    return new_user.id


async def update_profile(db: AsyncSession, user_id: uuid4, values: dict):
    query = update(Users).where(Users.id == user_id).values(**values)
    result = await db.execute(query)
    return result


async def login(db: AsyncSession, phone: str):
    """Get user by phone"""
    query = select(Users.id).where(Users.phone == phone)
    result = await db.execute(query)
    return result.mappings().first()


async def get_user_by_id(db: AsyncSession, user_id: uuid4):
    """Get user by ID"""
    query = select(Users.id).where(
        Users.id == user_id
    )
    result = await db.execute(query)
    return result.mappings().first()
