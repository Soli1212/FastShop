from sqlalchemy import Column, Integer, String, DateTime, UUID
from datetime import datetime
from sqlalchemy.orm import relationship
from uuid import uuid4
from Application.Database import BaseModel


class Users(BaseModel):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    fullname = Column(String(100), nullable=False)
    
    phone = Column(String(11), nullable=False, unique=True, index = True)
    
    email = Column(String(100), nullable=True, unique=True)
    
    password = Column(String(255), nullable=False)
    
    created_at = Column(DateTime, default = datetime.utcnow, nullable=False)

    last_password_change = Column(DateTime, default = datetime.utcnow, nullable=False)
    
    Addresses = relationship("Addresses", back_populates = "user")
    orders = relationship("Orders", back_populates="user")