
from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Stock(Base):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), unique=True)
    name = Column(String(50))
    price_today = Column(Integer)
    last_days_price = Column(Integer)
    volume = Column(Integer)
    #date

from pydantic import BaseModel, Field
############ pydantic mallien alustaminen -> varmentaa
class StockBase(BaseModel):
    ticker: str
    name: str
    price_today: int
    last_days_price: int
    volume: int
    

# class Portfolio(Base):
#     __tablename__ = 'salkku'
#     id = Column(Integer, primary_key=True, index=True)
#     stocks = Column(String)
#     value = Column(Integer)


