from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), unique=True)
    name = Column(String(50))
    price_today = Column(Integer)
    last_days_price = Column(Integer)
    volume = Column(Integer)
    date = Column(String(50))
    transactions = relationship("Transaction", back_populates="stock_data")

from pydantic import BaseModel, Field
############ pydantic mallien alustaminen -> varmentaa
class StockBase(BaseModel):
    ticker: str
    name: str
    price_today: int
    last_days_price: int
    volume: int
    date: str
 

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True, index=True)
    transactions = relationship("Transaction", back_populates="portfolio")
    portfolio_value = Column(Integer)


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock.id"))
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    stock_amount = Column(Integer)
    purchase_date = Column(String(50))

    stock_data = relationship("Stock", back_populates="transactions")
    portfolio = relationship("Portfolio", back_populates="transactions")