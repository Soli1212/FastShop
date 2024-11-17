from Application.Database import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from jdatetime import datetime

class Products(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), nullable=False, index=True)
    
    description = Column(String(500), nullable=False)
    
    sizes = Column(ARRAY(String), nullable=True)
    
    colors = Column(ARRAY(String), nullable=True)

    dimensions = Column(String, nullable=True) 
    
    price = Column(Integer, nullable=False)
    
    discounted_price = Column(Integer, nullable=True)
    
    inventory = Column(Boolean, nullable=False, default=True)
    
    new = Column(Boolean, nullable=False, default=True)
    
    lux = Column(Boolean, nullable=False, default=True)

    created_at = Column(String, default=lambda: datetime.now().strftime("%Y/%m/%d %H:%M:%S"), nullable=False)

    images = relationship("ProductImages", back_populates="product")