from fastapi import APIRouter, Depends, Path, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Auth import authorize
from Application.Database import get_db
from Application.Services import address_service
from Domain.schemas.address_schemas import NewAddress, UpdateAddress

Router = APIRouter()


@Router.get("/")
async def me(
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await address_service.my_addresses(db=db, user_id=auth["id"])


@Router.post("/new", status_code=status.HTTP_201_CREATED)
async def New_Address(
    Address: NewAddress,
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await address_service.new_address(db=db, address=Address, user_id=auth["id"])


@Router.delete("/delete/{Address_id}", status_code=status.HTTP_200_OK)
async def Delete_Address(
    Address_id: int = Path(gt=0),
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await address_service.delete_address(
        db=db, user_id=auth["id"], address_id=Address_id
    )


@Router.patch("/update/{Address_id}", status_code=status.HTTP_200_OK)
async def Update_Address(
    UAddress: UpdateAddress,
    Address_id: int = Path(gt=0),
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await address_service.update_address(
        db=db, user_id=auth["id"], address_id=Address_id, uaddress=UAddress
    )
