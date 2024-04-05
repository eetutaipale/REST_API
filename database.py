from sqlalchemy import Column, create_engine, Table, select, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

import time
import logging

# Log in credentials and connection URL-string as DATABASE_CONNECTION
load_dotenv()
SERVER_IP = os.getenv("SERVER_IP")
DRIVER = os.getenv("DRIVER")
DATABASE = os.getenv("DATABASE")
UID = os.getenv("UID")
PWD = os.getenv("PWD")
DATABASE_CONNECTION = f"mssql+pyodbc://{UID}:{PWD}@{SERVER_IP}/{DATABASE}?driver={DRIVER}"

# Engine and sessionmaker
engine = create_engine(DATABASE_CONNECTION, echo=True) # Creating an engine object to connect to database
metadata = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()













# Populate database with stockdata
def save_to_database(stock_data_list):
    print("Save to database in action...")
    # Set up logging configuration
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='database.log',
                        filemode='a')

    # Using the engine object for straight connection to DB
    connection = engine.connect()
    print(f"Conncetion opened to {DATABASE} @ {SERVER_IP}")
    stock_data_table = Table('stock_data', metadata,
        Column('id', int, primary_key=True),
        Column('name', str),
        Column('price', str),
        Column('volume', str),
        Column('previous_close_price', str)
    )
    # SQL query with SQLAlchemy methods
    if not metadata.tables.get('stock_data'):
        # Create the table if it doesn't exist
        stock_data_table = metadata.create_all()
        print("Table 'stock_data' created")

    for stock_data in stock_data_list:
        connection.execute(stock_data_table.insert().values(
            name=stock_data['name'],
            price=str(stock_data['price']),
            volume=str(stock_data['volume']),
            previous_close_price=str(stock_data['previous_close_price'])
        ))
    print("Closing connection...")
    connection.close()

# CREATE function, add new stock to portfolio, portfolio 1 - N stocks
def create_portfolio_item():
    return

# READ functions, read stockmarket and portfolio as different tabs
def get_portfolio():
    return
def get_stockmarket():
    return

# UPDATE function, if needed to add/buy more existing stock
def update_portfolio_item():
    return

# DELETE function, delete from portfolio
def delete_portfolio_item():
    return


