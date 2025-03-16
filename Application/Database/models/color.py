from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from Application.Database import Base

product_colors = Table(
    "product_colors",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("color_id", Integer, ForeignKey("colors.id"), primary_key=True),
)


class Colors(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True)
    hex_code = Column(String(7), unique=True, nullable=False)
    name = Column(String(50))

    products = relationship(
        "Products", secondary=product_colors, back_populates="colors"
    )

    inventories = relationship("ProductInventory", back_populates="color")
