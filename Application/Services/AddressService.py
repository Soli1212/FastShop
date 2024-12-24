from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import AddressRepositories
from Domain.schemas.AddressSchemas import (
    NewAddress,
    UpdateAddress
)
from Domain.Errors.address import (
    AddressLimit,
    NoAddressWasFound,
    InvalidProvince
)

IRANIAN_PROVINCES = [
    "البرز", "اردبیل", "بوشهر", "چهارمحال و بختیاری",
    "آذربایجان شرقی", "آذربایجان غربی", "اصفهان", "فارس",
    "گیلان", "گلستان", "همدان", "هرمزگان", "ایلام", "کرمان",
    "کرمانشاه", "خراسان جنوبی", "خراسان رضوی", "خراسان شمالی",
    "خوزستان", "کهگیلویه و بویراحمد", "کردستان", "لرستان",
    "مرکزی", "مازندران", "قزوین", "قم", "سمنان", 
    "سیستان و بلوچستان", "تهران", "یزد", "زنجان"
]

class AddressServices:
    
    @staticmethod
    async def New_Address(db: AsyncSession, Address: NewAddress, user_id: str):
        if await AddressRepositories.Get_Address_Count(db = db, user_id = user_id) >= 3:
            raise AddressLimit
        
        if Address.province not in IRANIAN_PROVINCES:
            raise InvalidProvince

        AddNewAddress = await AddressRepositories.Add_New_Address(
            db = db, NewAddress = Address, user_id = user_id
        )

        if AddNewAddress:
            return "The address has been successfully registered"
        

    @staticmethod
    async def Delete_Address(db: AsyncSession, user_id: str, address_id: int):

        if await AddressRepositories.Delete_Address(
            db = db, address_id = address_id, user_id = user_id
        ):
            return "The address has been successfully deleted."
        else:
            raise NoAddressWasFound
        

    @staticmethod
    async def Update_Address(db: AsyncSession, user_id: str, address_id: int, UAddress: UpdateAddress):
        if address := await AddressRepositories.Get_Address(db = db, address_id = address_id, user_id = user_id):

            for name, value in UAddress.dict(exclude_unset=True).items():
                setattr(address, name, value)

            return address
        else:
            raise NoAddressWasFound
    
    @staticmethod
    async def My_addresses(db: AsyncSession, user_id: int):
        return await AddressRepositories.Get_My_Addresses(db, user_id = user_id)




    