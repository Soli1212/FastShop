from Application.Database import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime

from .Tag import product_tags
class Products(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), nullable=False, index=True)

    description = Column(String(500), nullable=False)
    
    sizes = Column(ARRAY(Integer), nullable=True)
    
    colors = Column(ARRAY(String), nullable=True)

    dimensions = Column(String, nullable=True) 
    
    price = Column(Integer, nullable=False)
    
    discounted_price = Column(Integer, nullable=True)
    
    inventory = Column(Integer, nullable=False, default = 1)
    
    new = Column(Boolean, nullable=False, default=True)
    
    lux = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship("ProductImages", back_populates="product")
    tags = relationship("Tags", secondary=product_tags, back_populates = "products")