from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Auth import authorize
from Application.Database import get_db
from Application.Services import cart_service
from Domain.schemas.cart_schemas import CartItem, DeleteItem

Router = APIRouter()


@Router.post("/add")
async def Add_To_Cart(
    item: CartItem, auth: authorize = Depends(), db: AsyncSession = Depends(get_db)
):
    return await cart_service.add_to_cart(
        db=db, rds=auth["rds"], user_id=auth["id"], item=item
    )


@Router.post("/delete")
async def Delete_Product(
    item: DeleteItem, auth: authorize = Depends(), db: AsyncSession = Depends(get_db)
):
    return await cart_service.delete_product(
        db=db, rds=auth["rds"], user_id=auth["id"], item=item
    )


@Router.get("/")
async def cart(
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await cart_service.get_cart(db=db, rds=auth["rds"], user_id=auth["id"])
