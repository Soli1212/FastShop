import enum
from datetime import datetime

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Application.Database import BaseModel


class OrderStatusEnum(enum.Enum):
    pending = "pending"
    processing = "processing"
    delivered = "delivered"


class Orders(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    address_id = Column(
        Integer, ForeignKey("addresses.id", ondelete="RESTRICT"), nullable=True
    )

    discount_id = Column(
        Integer, ForeignKey("discounts.id", ondelete="SET NULL"), nullable=True
    )

    total_price = Column(Float, nullable=False)

    status = Column(
        Enum(OrderStatusEnum), default=OrderStatusEnum.pending, nullable=False
    )

    created_at = Column(String, default=datetime.utcnow, nullable=False)

    user = relationship("Users", back_populates="orders")
    address = relationship("Addresses", back_populates="orders")
    discount = relationship("Discounts", back_populates="orders")
    order_items = relationship("OrderItems", back_populates="orders")
