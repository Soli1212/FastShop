from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Auth import authorize
from Application.Database import get_db
from Application.Services import order_service
from Domain.schemas.order_schemas import Order
from utils import limiter

Router = APIRouter()


@Router.post("/prepare")
@limiter.limit("10/minute")
async def prepare(
    request: Request,
    order: Order,
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await order_service.prepare_order(
        db=db, rds=auth["rds"], user_id=auth["id"], order=order
    )


@Router.get("/confirmation")
async def confirmation(
    Request: Request, auth: authorize = Depends(), db: AsyncSession = Depends(get_db)
):
    return await order_service.order_confirmation(
        request=Request, user_id=auth["id"], db=db, rds=auth["rds"]
    )
