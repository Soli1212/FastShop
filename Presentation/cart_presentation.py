from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Auth import authorize
from Application.Database import get_db
from Application.Services import cart_service
from Domain.schemas.cart_schemas import CartItem, DeleteItem
from utils import limiter

Router = APIRouter()


@Router.post("/add")
@limiter.limit("3/minute")
async def Add_To_Cart(
    request: Request,
    item: CartItem,
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await cart_service.add_to_cart(
        db=db, rds=auth["rds"], user_id=auth["id"], item=item
    )


@Router.post("/delete")
@limiter.limit("5/minute")
async def Delete_Product(
    request: Request,
    item: DeleteItem,
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
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
