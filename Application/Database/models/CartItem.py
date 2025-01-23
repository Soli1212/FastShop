from Application.Database import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, UUID, String
from sqlalchemy.orm import relationship

class CartItems(BaseModel):
    __tablename__ = "cartItems"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id", ondelete='CASCADE'), nullable = False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
    size = Column(Integer, nullable=True)
    color = Column(String, nullable=True)

    quantity = Column(Integer, nullable=False, default = 1)

    products = relationship("Products")
    User = relationship("Users", back_populates = "Cart") 

