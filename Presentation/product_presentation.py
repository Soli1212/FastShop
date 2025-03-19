from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database import get_db
from Application.Services import product_service

Router = APIRouter()


@Router.get("/luxuries")
async def luxuries_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await product_service.get_filtered_products(
        db=db, offset=page, filter_type=product_service.ProductFilterType.LUX
    )


@Router.get("/new")
async def new_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await product_service.get_filtered_products(
        db=db, offset=page, filter_type=product_service.ProductFilterType.NEW
    )


@Router.get("/best-selling")
async def best_selling_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await product_service.get_filtered_products(
        db=db, offset=page, filter_type=product_service.ProductFilterType.best_selling
    )


@Router.get("/discounted")
async def discounted_products(
    page: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await product_service.get_filtered_products(
        db=db, offset=page, filter_type=product_service.ProductFilterType.DISCOUNTED
    )


@Router.get("/random/{filter_random}")
async def random_products(filter_random, db: AsyncSession = Depends(get_db)):
    return await product_service.get_random_products(db=db, filter_type=filter_random)


@Router.get("/{product_id}")
async def Products(product_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await product_service.load_product(db=db, product_id=product_id)
