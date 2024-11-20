from Application.Database.models import Users
from Domain.schemas.UserSchemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import exists

class UserRepositories:

    @staticmethod
    async def Create_User(db: AsyncSession, NewUserData: UserCreate):
        "add new user"
        NewUser = Users(**NewUserData.dict(exclude_unset=True))
        db.add(instance = NewUser)
        await db.flush()
        return NewUser.id

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
    
    