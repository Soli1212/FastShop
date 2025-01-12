from fastapi import Request
from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi import status
from fastapi import Path
from typing import Optional
from Application.Database import get_db
from Application.Services import TagServices

from sqlalchemy.ext.asyncio import AsyncSession



Router = APIRouter()


@Router.get("/")
async def me(
    db: AsyncSession = Depends(get_db)
):
    return await TagServices.Get_Tags(db = db)

@Router.get("/{tag_id}")
async def tags(
    request: Request,
    db: AsyncSession = Depends(get_db),
    tag_id: int = Path(gt=0),
    min_price: int = Query(default = None, ge=35000),
    max_price: int = Query(default = None, le=2000000, ge=35000),
    size: Optional[str] = Query(default = None, pattern=r'^\d{2}(-\d{2})*$'),
    color: Optional[str] = Query(default = None, pattern=r'^[a-zA-Z]+(-[a-zA-Z]+)*$'),
    page: int = Query(default = 0, ge=0)
    ):
        return await TagServices.Get_Tag_Products(db = db, filters=request.query_params, tag_id=tag_id)
