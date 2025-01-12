from Application.Database.models import Addresses

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from sqlalchemy.sql import exists

from Domain.schemas.AddressSchemas import NewAddress


class AddressRepositories:

    @staticmethod
    async def Get_Address_Count(db: AsyncSession, user_id: str):
        query = select(func.count()).select_from(Addresses).where(
            Addresses.user_id == user_id
        )

        result = await db.execute(query)
        return result.scalar()
    

    @staticmethod
    async def Add_New_Address(db: AsyncSession, NewAddress: NewAddress, user_id: str):
        Address = Addresses(
            user_id = user_id,
            **NewAddress.dict(exclude_unset=True)
        )

        db.add(instance = Address)
        return True


    @staticmethod
    async def Delete_Address(db: AsyncSession, address_id: int, user_id: str):
        query = delete(Addresses).where(
            Addresses.id == address_id, Addresses.user_id == user_id
        ).returning(Addresses.id)

        result = await db.execute(query)
        return result.scalar_one_or_none()
    

    @staticmethod
    async def Get_Address(db: AsyncSession, address_id: int, user_id: str):
        query = select(Addresses).where(
            Addresses.id == address_id, Addresses.user_id == user_id
        )
        
        result = await db.execute(query)
        return result.scalars().first()
    

    @staticmethod
    async def Get_My_Addresses(db: AsyncSession, user_id: str):
        query = select(Addresses).where(Addresses.user_id == user_id)

        result = await db.execute(query)
        return result.scalars().all()
    

