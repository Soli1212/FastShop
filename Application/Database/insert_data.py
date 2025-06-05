import random
from faker import Faker
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Table, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

# Initialize Faker for generating fake data
fake = Faker('fa_IR')

# Database setup
DATABASE_URL = "postgresql+psycopg2://postgres:Solix.e30v90@localhost:5432/postgres"  # Replace with your actual DB URL
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Association tables
product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

product_colors = Table(
    "product_colors",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("color_id", Integer, ForeignKey("colors.id"), primary_key=True)
)

# Tags model
class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=True)
    children = relationship("Tags", remote_side=[id])
    products = relationship("Products", secondary=product_tags, back_populates="tags")

# Products model
class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    sizes = Column(ARRAY(Integer), nullable=True)
    dimensions = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    discounted_price = Column(Integer, nullable=True, index=True)
    inventory = Column(Boolean, nullable=False, default=True)
    new = Column(Boolean, nullable=False, default=True, index=True)
    lux = Column(Boolean, nullable=False, default=False, index=True)
    best_selling = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    images = relationship("ProductImages", back_populates="product")
    tags = relationship("Tags", secondary=product_tags, back_populates="products")
    inventories = relationship("ProductInventory", back_populates="product")
    colors = relationship("Colors", secondary=product_colors, back_populates="products")

# ProductInventory model
class ProductInventory(Base):
    __tablename__ = "product_inventories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    color_id = Column(Integer, ForeignKey("colors.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True, index=True)
    size = Column(Integer, nullable=True)
    inventory = Column(Integer, nullable=False, default=1)
    product = relationship("Products", back_populates="inventories")
    color = relationship("Colors", back_populates="inventories")

# ProductImages model
class ProductImages(Base):
    __tablename__ = "productImages"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    url = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    color_id = Column(Integer, ForeignKey("colors.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    is_main = Column(Boolean, default=False, index=True)
    product = relationship("Products", back_populates="images")
    color = relationship("Colors")

# Colors model
class Colors(Base):
    __tablename__ = "colors"
    id = Column(Integer, primary_key=True, index=True)
    hex_code = Column(String(7), unique=True, nullable=False)
    name = Column(String(50))
    products = relationship("Products", secondary=product_colors, back_populates="colors")
    inventories = relationship("ProductInventory", back_populates="color")

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Sample data for tags
tag_names = ["لباس", "ورزشی", "رسمی", "کژوال", "زمستانی", "تابستانی", "مد روز", "کلاسیک"]
tags = []

# Insert tags
for name in tag_names:
    tag = Tags(name=name)
    session.add(tag)
    tags.append(tag)
session.commit()

# Sample data for colors
colors_data = [
    {"name": "قرمز", "hex_code": "#FF0000"},
    {"name": "آبی", "hex_code": "#0000FF"},
    {"name": "سبز", "hex_code": "#00FF00"},
    {"name": "مشکی", "hex_code": "#000000"},
    {"name": "سفید", "hex_code": "#FFFFFF"},
]
colors = []

# Insert colors
for color_data in colors_data:
    color = Colors(name=color_data["name"], hex_code=color_data["hex_code"])
    session.add(color)
    colors.append(color)
session.commit()

# Generate and insert 50 products
for _ in range(50):
    # Create a product
    product = Products(
        name=fake.word() + " " + random.choice(["تی‌شرت", "شلوار", "کفش", "کت"]),
        description=fake.text(max_nb_chars=200),
        sizes=random.sample(range(36, 46), k=random.randint(1, 5)),
        dimensions=f"{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(10, 100)}",
        price=random.randint(100000, 1000000),
        discounted_price=random.randint(80000, 900000) if random.choice([True, False]) else None,
        inventory=random.choice([True, False]),
        new=random.choice([True, False]),
        lux=random.choice([True, False]),
        best_selling=random.choice([True, False]),
        created_at=datetime.utcnow()
    )
    session.add(product)
    session.flush()  # Get product ID

    # Assign random tags to the product
    product.tags = random.sample(tags, k=random.randint(1, 3))

    # Assign random colors to the product
    product.colors = random.sample(colors, k=random.randint(1, 3))

    # Add product inventory
    for color in product.colors:
        inventory = ProductInventory(
            product_id=product.id,
            color_id=color.id,
            size=random.choice(product.sizes) if product.sizes else None,
            inventory=random.randint(0, 100)
        )
        session.add(inventory)

    # Add product images
    for color in product.colors:
        image = ProductImages(
            url=fake.image_url(),
            product_id=product.id,
            color_id=color.id,
            is_main=random.choice([True, False])
        )
        session.add(image)

# Commit all changes
session.commit()

# Close session
session.close()