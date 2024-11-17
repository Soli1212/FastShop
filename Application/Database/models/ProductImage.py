from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Application.Database import BaseModel

class ProductImages(BaseModel):
    __tablename__ = 'productImages'

    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    url = Column(String, nullable=False)
    
    product_id = Column(Integer, 
    
    ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    product = relationship("Products", back_populates="images")