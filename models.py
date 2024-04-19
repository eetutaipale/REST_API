from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from pydantic import BaseModel, Field

# Stock model
class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10))
    name = Column(String(50))
    price_today = Column(Integer)
    last_days_price = Column(Integer)
    volume = Column(Integer)
    date = Column(String(50))
    transactions = relationship("Transaction", back_populates="stocks")

# Stock pydantic basemodel, where all 
class StockCreate(BaseModel):
    ticker: str
    name: str
    price_today: int
    last_days_price: int
    volume: int
    date: str

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True, index=True)
    portfolio_name = Column(String(50))
    portfolio_value = Column(Integer)

    transactions = relationship("Transaction", back_populates="portfolios")

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock.id"))
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    stock_amount = Column(Integer)
    purchase_date = Column(String(50))

    stocks = relationship("Stock", back_populates="transactions")
    portfolios = relationship("Portfolio", back_populates="transactions")

class TransactionCreate(BaseModel):
    ticker: str
    stock_id: int
    portfolio_id: int
    stock_amount: int
    purchase_date: str
############ pydantic mallien alustaminen -> varmentaa


class PortfolioBase(BaseModel):
    portfolio_name: str
    portfolio_value: int

class Base(DeclarativeBase):
    pass
    