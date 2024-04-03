from sqlalchemy import Boolean, Column, Integer, String
from database import base


class Stock(base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10))
    name = Column(String(50))
    price_today = Column(Integer)
    Last_days_price = Column(Integer)
    Volume = Column(Integer)
    
class salkku(base):
    __tablename__ = 'salkku'
    id = Column(Integer, primary_key= True, index=True)
    stocks = Column(Integer, Integer)
    Value = Column(Integer)
