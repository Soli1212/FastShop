from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Application.Database import BaseModel


class Discounts(BaseModel):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, unique=True, index=True, nullable=False)

    description = Column(String)

    discount_percentage = Column(Float, nullable=False)

    min_order_value = Column(Float, default=0)

    start_date = Column(DateTime, default=datetime.utcnow)

    end_date = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    orders = relationship("Orders", back_populates="discount")
