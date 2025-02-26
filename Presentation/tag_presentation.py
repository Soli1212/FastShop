from typing import Optional

from fastapi import APIRouter, Depends, Path, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database import get_db
from Application.Services import tag_service

Router = APIRouter()


@Router.get("/")
async def me(db: AsyncSession = Depends(get_db)):
    return await tag_service.get_tags(db=db)


@Router.get("/{tag_id}")
async def tags(
    request: Request,
    db: AsyncSession = Depends(get_db),
    tag_id: int = Path(gt=0),
    min_price: Optional[int] = Query(default=None, ge=35000),
    max_price: Optional[int] = Query(default=None, le=2000000, ge=35000),
    size: Optional[str] = Query(default=None, pattern=r"^\d{2}(-\d{2})*$"),
    color: Optional[str] = Query(
        default=None, pattern=r"^([0-9A-Fa-f]{6})(-[0-9A-Fa-f]{6})*-?$|^$"
    ),
    order_by: Optional[str] = Query(default="new"),
    page: int = Query(default=0, ge=0),
):
    return await tag_service.get_tag_products(
        db=db, filters=dict(request.query_params), tag_id=tag_id, order_by=order_by
    )
