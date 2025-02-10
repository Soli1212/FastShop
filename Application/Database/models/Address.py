from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Application.Database import Base


class Addresses(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="Cascade", onupdate="Cascade"),
        nullable=False,
        index=True,
    )

    province = Column(String(100), nullable=False)

    city = Column(String(100), nullable=False)

    street = Column(String, nullable=False)

    postal_code = Column(String(10), nullable=True)

    recipient_phone = Column(String(11), nullable=False)

    full_address = Column(String, nullable=False)

    user = relationship("Users", back_populates="Addresses")
    orders = relationship("Orders", back_populates="address")
