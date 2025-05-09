from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship

from Application.Database import Base


class Discounts(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(6), unique=True, index=True, nullable=False)

    discount_percentage = Column(Float, nullable=False)

    min_order_value = Column(Float, default=0)

    start_date = Column(DateTime, default=datetime.utcnow)

    end_date = Column(DateTime, nullable=False)

    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    orders = relationship("Orders", back_populates="discount")
