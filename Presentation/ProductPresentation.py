from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database import get_db
from Application.Services import ProductService

Router = APIRouter()


@Router.get("/luxuries")
async def Luxuries_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await ProductService.lux_products(db=db, offset=page)


@Router.get("/new")
async def New_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await ProductService.new_products(db=db, offset=page)


@Router.get("/discounted")
async def discounted_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await ProductService.discounted_products(db=db, offset=page)


@Router.get("/{product_id}")
async def Products(product_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await ProductService.load_product(db=db, product_id=product_id)
