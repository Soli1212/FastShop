from uuid import uuid4

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import load_only
from sqlalchemy.sql import exists

from Application.Database.models import Users


async def create_user(db: AsyncSession, user_phone: str, user_password: str):
    """Add new user"""
    new_user = Users(phone=user_phone, password=user_password)
    db.add(new_user)
    await db.flush()
    return new_user.id


async def update_profile(db: AsyncSession, user_id: uuid4, values: dict):
    query = update(Users).where(Users.id == user_id).values(**values)
    result = await db.execute(query)
    return result


async def login(db: AsyncSession, phone: str):
    """Get user by phone"""
    query = select(Users.id, Users.password).where(Users.phone == phone)
    result = await db.execute(query)
    return result.mappings().first()


async def get_user_by_id(db: AsyncSession, user_id: uuid4):
    """Get user by ID"""
    query = select(Users.id, Users.phone, Users.fullname, Users.email).where(
        Users.id == user_id
    )
    result = await db.execute(query)
    return result.mappings().first()


async def get_user_by_phone(db: AsyncSession, phone: str):
    query = (
        select(Users)
        .options(load_only(Users.id, Users.password, Users.last_password_change))
        .where(Users.phone == phone)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_last_password_change(db: AsyncSession, user_id: uuid4):
    query = select(Users.last_password_change).where(Users.id == user_id)
    result = await db.execute(query)
    return result.mappings().first()


async def check_exists_phone(db: AsyncSession, phone: str) -> bool:
    """Check the existence of a phone number"""
    query = select(exists().where(Users.phone == phone))
    result = await db.execute(query)
    return result.scalar()


async def check_exists_email(db: AsyncSession, email: str):
    """Check the existence of an email"""
    query = select(exists().where(Users.email == email))
    result = await db.execute(query)
    return result.scalar()
