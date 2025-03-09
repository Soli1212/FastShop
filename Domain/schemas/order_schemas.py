from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Order(BaseModel):
    address_id: int = Field(...)
    discount_code: Optional[str] = Field(None)


class OrderStatusEnum(Enum):
    pending = "pending"
    processing = "processing"
    delivered = "delivered"


class NewOrder(BaseModel):
    address_id: int = Field(...)
    discount_id: Optional[str] = Field(default=None)
    total_price: float = Field()
    status: OrderStatusEnum = Field(default=OrderStatusEnum.pending)
