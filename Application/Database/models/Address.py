from Application.Database import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Addresses(BaseModel):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete = "Cascade", onupdate = "Cascade"), nullable=False)

    province = Column(String(100), nullable=False)

    city = Column(String(100), nullable=False)

    street = Column(String, nullable=False)

    postal_code = Column(String(10), nullable=True)

    recipient_phone = Column(String(10), nullable=False)

    full_address = Column(String, nullable=False) 

    user = relationship("Users", back_populates = "Addresses")
    orders = relationship("Orders", back_populates = "address")