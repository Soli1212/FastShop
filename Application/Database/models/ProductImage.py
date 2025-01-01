from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from Application.Database import BaseModel

class ProductImages(BaseModel):
    __tablename__ = 'productImages'

    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    url = Column(String, nullable=False)
    
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    is_main = Column(Boolean, default=False)

    product = relationship("Products", back_populates="images")