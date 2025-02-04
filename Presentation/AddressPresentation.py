from fastapi import APIRouter, Depends, Path, Request, Response, status

from Application.Database import get_db
from Application.Auth import authorize
from Application.Services import AddressService
from Domain.schemas.AddressSchemas import NewAddress, UpdateAddress

Router = APIRouter()


@Router.get("/")
async def me(auth: authorize = Depends()):
    return await AddressService.my_addresses(db=auth["db"], user_id=auth["id"])


@Router.post("/new", status_code=status.HTTP_201_CREATED)
async def New_Address(
    Address: NewAddress,
    auth: authorize = Depends(),
):
    return await AddressService.new_address(
        db=auth["db"], address=Address, user_id=auth["id"]
    )


@Router.delete("/delete/{Address_id}", status_code=status.HTTP_200_OK)
async def Delete_Address(Address_id: int = Path(gt=0), auth: authorize = Depends()):
    return await AddressService.delete_address(
        db=auth["db"], user_id=auth["id"], address_id=Address_id
    )


@Router.patch("/update/{Address_id}", status_code=status.HTTP_200_OK)
async def Update_Address(
    UAddress: UpdateAddress,
    Address_id: int = Path(gt=0),
    auth: authorize = Depends(),
):
    return await AddressService.update_address(
        db=auth["db"], user_id=auth["id"], address_id=Address_id, uaddress=UAddress
    )
