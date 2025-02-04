from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Application.Database import BaseModel


class ProductInventory(BaseModel):
    __tablename__ = "product_inventories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )

    color = Column(String, nullable=True)
    size = Column(Integer, nullable=True)

    inventory = Column(Integer, nullable=False, default=1)

    product = relationship("Products", back_populates="inventories")
