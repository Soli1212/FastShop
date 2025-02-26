from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Auth import authorize
from Application.Database import get_db
from Application.Services import order_service
from Domain.schemas.order_schemas import Order

Router = APIRouter()


@Router.post("/prepare")
async def prepare(
    order: Order,
    auth: authorize = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await order_service.prepare_order(
        db=db, rds=auth["rds"], user_id=auth["id"], order=order
    )
