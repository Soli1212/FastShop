from datetime import datetime
from Application.Database import BaseModel
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
import enum


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"

class Users(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    fullname = Column(String(100), nullable=False)

    phone = Column(String(11), nullable=False, unique=True, index=True)

    email = Column(String(100), nullable=True, unique=True)

    gender = Column(Enum(GenderEnum), nullable=True)
    
    age = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default = datetime.now, nullable=False)

    Addresses = relationship("Addresses", back_populates = "user")

    orders = relationship("Orders", back_populates="user")