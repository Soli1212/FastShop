from fastapi import APIRouter, Depends, Path, Request, Response, status

from Application.Database import get_db
from Application.Auth import authorize
from Application.Services import CartService
from Domain.schemas.Cart import CartItem, DeleteItem

Router = APIRouter()


@Router.post("/add")
async def Add_To_Cart(
    item: CartItem,
    auth: authorize = Depends(),
):
    return await CartService.add_to_cart(
        db=auth["db"], rds=auth["rds"], user_id=auth["id"], item=item
    )


@Router.post("/delete")
async def Delete_Product(item: DeleteItem, auth: authorize = Depends()):
    return await CartService.delete_product(
        rds=auth["rds"], user_id=auth["id"], item=item
    )


@Router.get("/")
async def cart(auth: authorize = Depends()):
    return await CartService.get_cart(
        db=auth["db"], rds=auth["rds"], user_id=auth["id"]
    )
