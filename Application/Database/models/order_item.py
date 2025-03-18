from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Application.Database import Base


class OrderItems(Base):
    __tablename__ = "orderItems"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    size = Column(Integer, nullable=True)

    color_id = Column(
        Integer,
        ForeignKey("colors.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )

    quantity = Column(Integer, default=1, nullable=False)

    price = Column(Float, nullable=False)

    total_price = Column(Float, nullable=False)

    orders = relationship("Orders", back_populates="order_items")
    product = relationship("Products")
    color = relationship("Colors")
