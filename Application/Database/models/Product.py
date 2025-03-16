from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from Application.Database import Base

from .color import product_colors
from .tag import product_tags


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    name = Column(String(100), nullable=False, index=True)

    description = Column(String(500), nullable=False)

    sizes = Column(ARRAY(Integer), nullable=True)

    dimensions = Column(String, nullable=True)

    price = Column(Integer, nullable=False)

    discounted_price = Column(Integer, nullable=True, index=True)

    inventory = Column(Boolean, nullable=False, default=True)

    new = Column(Boolean, nullable=False, default=True, index=True)

    lux = Column(Boolean, nullable=False, default=False, index=True)

    best_selling = Column(Boolean, nullable=False, default=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    images = relationship("ProductImages", back_populates="product")
    tags = relationship("Tags", secondary=product_tags, back_populates="products")
    inventories = relationship("ProductInventory", back_populates="product")
    colors = relationship("Colors", secondary=product_colors, back_populates="products")
