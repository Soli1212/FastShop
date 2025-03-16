from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Application.Database import Base


class ProductInventory(Base):
    __tablename__ = "product_inventories"

    id = Column(Integer, primary_key=True, autoincrement=True)

    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )

    color_id = Column(
        Integer,
        ForeignKey("colors.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    size = Column(Integer, nullable=True)
    inventory = Column(Integer, nullable=False, default=1)

    product = relationship("Products", back_populates="inventories")
    color = relationship("Colors", back_populates="inventories")
