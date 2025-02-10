from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import AddressRepository
from Domain.Errors.address import AddressLimit, InvalidProvince, NoAddressWasFound
from Domain.schemas.AddressSchemas import NewAddress, UpdateAddress

IRANIAN_PROVINCES = [
    "البرز",
    "اردبیل",
    "بوشهر",
    "چهارمحال و بختیاری",
    "آذربایجان شرقی",
    "آذربایجان غربی",
    "اصفهان",
    "فارس",
    "گیلان",
    "گلستان",
    "همدان",
    "هرمزگان",
    "ایلام",
    "کرمان",
    "کرمانشاه",
    "خراسان جنوبی",
    "خراسان رضوی",
    "خراسان شمالی",
    "خوزستان",
    "کهگیلویه و بویراحمد",
    "کردستان",
    "لرستان",
    "مرکزی",
    "مازندران",
    "قزوین",
    "قم",
    "سمنان",
    "سیستان و بلوچستان",
    "تهران",
    "یزد",
    "زنجان",
]


async def new_address(db: AsyncSession, address: NewAddress, user_id: UUID):
    if await AddressRepository.get_address_count(db=db, user_id=user_id) >= 3:
        raise AddressLimit

    if address.province not in IRANIAN_PROVINCES:
        raise InvalidProvince

    added_address = await AddressRepository.add_new_address(
        db=db, new_address=address, user_id=user_id
    )

    if added_address:
        return await my_addresses(db=db, user_id=user_id)


async def delete_address(db: AsyncSession, user_id: UUID, address_id: int):
    if await AddressRepository.delete_address(
        db=db, address_id=address_id, user_id=user_id
    ):
        return await my_addresses(db=db, user_id=user_id)
    else:
        raise NoAddressWasFound


async def update_address(
    db: AsyncSession, user_id: UUID, address_id: int, uaddress: UpdateAddress
):
    if address := await AddressRepository.get_address(
        db=db, address_id=address_id, user_id=user_id
    ):
        for name, value in uaddress.dict(exclude_unset=True).items():
            setattr(address, name, value)
        return address
    else:
        raise NoAddressWasFound


async def my_addresses(db: AsyncSession, user_id: UUID):
    Addresses = await AddressRepository.get_my_addresses(db, user_id=user_id)

    return [i["Addresses"] for i in Addresses]
