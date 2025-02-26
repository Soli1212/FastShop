from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database import get_db
from Application.Services import product_service

Router = APIRouter()


@Router.get("/luxuries")
async def Luxuries_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await product_service.lux_products(db=db, offset=page)


@Router.get("/new")
async def New_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await product_service.new_products(db=db, offset=page)


@Router.get("/discounted")
async def discounted_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await product_service.discounted_products(db=db, offset=page)


@Router.get("/{product_id}")
async def Products(product_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await product_service.load_product(db=db, product_id=product_id)
