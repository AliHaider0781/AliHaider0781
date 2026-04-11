from __future__ import annotations

from sqlalchemy import Column, Date, Integer, Numeric, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    segment = Column(String)
    signup_date = Column(Date)
    region = Column(String)
    channel = Column(String)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String)
    cost_price = Column(Numeric)
    retail_price = Column(Numeric)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String)
    order_date = Column(Date)
    product_id = Column(String)
    quantity = Column(Integer)
    discount = Column(Numeric)
    channel = Column(String)
    warehouse = Column(String)


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    warehouse = Column(String)
    product_id = Column(String)
    on_hand = Column(Integer)
    reorder_point = Column(Integer)
    lead_time_days = Column(Integer)


class MarketingSpend(Base):
    __tablename__ = "marketing_spend"

    campaign_id = Column(String, primary_key=True, index=True)
    channel = Column(String)
    month = Column(Date)
    spend = Column(Numeric)
    attributed_revenue = Column(Numeric)
    impressions = Column(Integer)
    clicks = Column(Integer)
    conversions = Column(Integer)


class Logistics(Base):
    __tablename__ = "logistics"

    shipment_id = Column(String, primary_key=True, index=True)
    order_id = Column(String)
    carrier = Column(String)
    status = Column(String)
    ship_date = Column(Date)
    delivery_date = Column(Date)
    warehouse = Column(String)
    region = Column(String)
    tracking_number = Column(String)
