from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from Application.Database import BaseModel


product_tags = Table(
    "product_tags",

    BaseModel.metadata,
    
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Tags(BaseModel):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    
    name = Column(String(50), unique=True, nullable=False)

    parent_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    
    parent = relationship("Tags", remote_side=[id], backref="children")
