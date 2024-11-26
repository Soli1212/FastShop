from Application.Database.models import Users

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
        await db.flush()
        return NewUser.id
    

    @staticmethod
    async def get_User_ID_By_Phone(db: AsyncSession, phone: str):
        "get user by phone"
        query = select(Users.id).where(Users.phone == phone)
        result = await db.execute(query)
        return result.scalars().first()


    @staticmethod
    async def Get_User_By_ID(db: AsyncSession, user_id: int):
        "get user by id"
        query = select(Users).where(Users.id == user_id)
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
    
    @staticmethod
    async def Check_Exists_ID(db: AsyncSession, user_id: str):
        "Checking the existence of id"
        query = select(exists().where(Users.id == user_id))
        result = await db.execute(query)
        return result.scalar()
    
    
    