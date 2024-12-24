from fastapi import Request
from fastapi import Response
from fastapi import Depends
from fastapi import APIRouter
from fastapi import status
from fastapi import Path

from Application.Database import get_db
from Application.Services import AddressServices

from Application.Auth import Authorize

from sqlalchemy.ext.asyncio import AsyncSession

from Domain.schemas.AddressSchemas import NewAddress
from Domain.schemas.AddressSchemas import AddressID
from Domain.schemas.AddressSchemas import UpdateAddress


Router = APIRouter()


@Router.get("/")
async def me(
    auth: Authorize = Depends()
):
    return await AddressServices.My_addresses(db = auth["db"], user_id = auth["id"])


@Router.post("/new", status_code = status.HTTP_201_CREATED)
async def New_Address(
    Address: NewAddress,
    auth: Authorize = Depends(),
):
    return await AddressServices.New_Address(
        db = auth["db"], Address = Address, user_id=auth["id"]
    )


@Router.delete("/delete/{Address_id}", status_code = status.HTTP_200_OK)
async def Delete_Address(
    Address_id: int = Path(gt = 0),
    auth: Authorize = Depends()
):
    return await AddressServices.Delete_Address(
        db = auth["db"], user_id = auth["id"], address_id = Address_id
    )


@Router.patch("/update/{Address_id}", status_code = status.HTTP_200_OK)
async def Update_Address(
    UAddress: UpdateAddress,
    Address_id: int = Path(gt = 0),
    auth: Authorize = Depends(),
):
    return await AddressServices.Update_Address(
        db = auth["db"], user_id = auth["id"], 
        address_id = Address_id, UAddress = UAddress
    )
