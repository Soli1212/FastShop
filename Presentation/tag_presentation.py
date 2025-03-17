from typing import Optional

from fastapi import APIRouter, Depends, Path, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database import get_db
from Application.Services import tag_service

Router = APIRouter()


@Router.get("/")
async def me(db: AsyncSession = Depends(get_db)):
    return await tag_service.get_tags(db=db)


# routes/tags.py
@Router.get("/{tag_id}")
async def tags(
    request: Request,
    db: AsyncSession = Depends(get_db),
    tag_id: int = Path(gt=0),
    min_price: Optional[int] = Query(default=None, ge=35000),
    max_price: Optional[int] = Query(default=None, le=2000000, ge=35000),
    size: Optional[str] = Query(default=None, pattern=r"^\d{2}(-\d{2})*$"),
    color: Optional[str] = Query(default=None),
    order_by: Optional[str] = Query(default="deafult"),
    page: int = Query(default=0, ge=0),
):
    return await tag_service.get_tag_products(
        db=db,
        tag_id=tag_id,
        min_price=min_price,
        max_price=max_price,
        size=size,
        color=color,
        order_by=order_by,
        page=page,
        limit=2,
    )
