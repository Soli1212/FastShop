from Application.Database.models import Users
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import exists

from Domain.schemas.UserSchemas import UserCreate


class UserRepositories:

    @staticmethod
    async def Create_User(db: AsyncSession, NewUserData: UserCreate):
        "add new user"
        NewUser = Users(**NewUserData.dict(exclude_unset=True))
        db.add(instance = NewUser)
        
        await db.commit()
        await db.flush()
        
        return NewUser.id

    @staticmethod
    async def Login(db: AsyncSession, phone: str):
        "get user by phone"
        query = query = select(Users.id, Users.password).where(Users.phone == phone)
        result = await db.execute(query)
        return result.fetchone()

    @staticmethod
    async def Get_User_By_ID(db: AsyncSession, user_id: uuid4):
        "get user by id"
        query = select(Users.id, Users.phone, Users.fullname, Users.email).where(Users.id == user_id)
        result = await db.execute(query)
        return result.fetchone()
    
    @staticmethod
    async def Get_User_By_Phone(db: AsyncSession, phone: str):
        query = select(Users).where(Users.phone == phone)
        result = await db.execute(query)
        return result.scalars().first()
    
    @staticmethod
    async def Get_User_Last_Password_Change(db: AsyncSession, user_id: uuid4):
        query = select(Users.last_password_change).where(Users.id == user_id)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def Check_Exists_Phone(db: AsyncSession, phone: str) -> bool: 
        "Checking the existence of a phone number" 
        query = select(exists().where(Users.phone == phone))
        result = await db.execute(query)
        return result.scalar()
    
    @staticmethod
    async def Check_Exists_Email(db: AsyncSession, email: str):
        "Checking the existence of email"
        query = select(exists().where(Users.email == email))
        result = await db.execute(query)
        return result.scalar()
    