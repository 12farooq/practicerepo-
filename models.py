from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DECIMAL, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()



class Customer(Base):
    __tablename__ = 'Customers'

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)  # Add unique constraint
    password = Column(String(255), unique=True, nullable=False)
    shipping_address = Column(Text)
    billing_address = Column(Text) 


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), index=True)
    description = Column(String(255))
    price = Column(Float)
    stock_quantity = Column(Integer)
    image_url = Column(String(255))
    #category_id = Column(Integer, ForeignKey("categories.category_id")) 


# class Category(Base):
#     __tablename__ = "categories"

#     category_id = Column(Integer, primary_key=True, index=True, nullable=True)
#     category_name = Column(String(255), unique=True, index=True)

#     products = relationship("Product", back_populates="category")










