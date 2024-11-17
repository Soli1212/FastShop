from Application.Database import BaseModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

class CartItems(BaseModel):
    __tablename__ = "cartItems"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id", ondelete='CASCADE'), nullable=False)

    quantity = Column(Integer, nullable=False, default = 1)

    product = relationship("Products")

