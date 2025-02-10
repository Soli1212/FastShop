from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from Application.Database import Base

product_tags = Table(
    "product_tags",
    Base.metadata,
    Column(
        "product_id",
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    parent_id = Column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=True
    )

    children = relationship("Tags", remote_side=[parent_id])
    products = relationship("Products", secondary=product_tags, back_populates="tags")
