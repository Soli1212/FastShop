from fastapi import Depends
from fastapi import APIRouter
from fastapi import Path
from fastapi import Query

from Application.Database import get_db
from Application.Services import ProductServices
from sqlalchemy.ext.asyncio import AsyncSession



Router = APIRouter()

@Router.get("/view/{product_id}")
async def Products(product_id : int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await ProductServices.load_product(db = db, product_id = product_id)

@Router.get("/luxuries")
async def Luxuries_products(
    page: int = Query(default = 0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await ProductServices.lux_products(db = db, offset = page)

@Router.get("/new")
async def New_products(
    page: int = Query(default = 0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await ProductServices.new_products(db = db, offset = page)

@Router.get("/discounted")
async def discounted_products(
    page: int = Query(default = 0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await ProductServices.discounted_products(db = db, offset = page)