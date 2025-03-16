from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Application.Database import Base


class ProductImages(Base):
    __tablename__ = "productImages"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    url = Column(String, nullable=False)

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    color_id = Column(
        Integer,
        ForeignKey("colors.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    is_main = Column(Boolean, default=False, index=True)

    product = relationship("Products", back_populates="images")
    color = relationship("Colors")
