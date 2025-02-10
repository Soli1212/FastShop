from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from Application.Database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    fullname = Column(String(100), nullable=True)

    phone = Column(String(11), nullable=False, unique=True, index=True)

    email = Column(String(100), nullable=True, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    Addresses = relationship("Addresses", back_populates="user")
    orders = relationship("Orders", back_populates="user")
