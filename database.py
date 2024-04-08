from typing import Self
from sqlalchemy import URL, Column, Inspector, create_engine, Table, func, select, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import models
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

engine_str = URL.create(
    drivername="mssql+pyodbc",
    username="meklari",
    password="Salasana!",
    host="sqlserverest.database.windows.net",
    port=1433,
    database="Stockdb",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "TrustServerCertificate": "no",
        "Connection Timeout": "30",
        "Encrypt": "yes",
    },
)

# Engine and sessionmaker
engine = create_engine(engine_str, echo=True) # Creating an engine object to connect to database
metadata = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base and making a table to database.
Base = declarative_base()
try:
    inspector = inspect(engine)
    if not inspector.has_table("stock_data"): # Logic works properly now in with inspector=inspect(engine)
        Base.metadata.create_all(bind=engine) # Create the table if it doesn't exist
        print("Table 'stock_data' created from database.py")
    else:
        print("Table \"stock_data\" exists, not creating new.")

except Exception as e:
    print("Error: ", e)





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
        print("Table 'stock_data' created from save_to_database")

    for stock_data in stock_data_list:
        connection.execute(stock_data_table.insert().values(
            name=stock_data['name'],
            price=str(stock_data['price']),
            volume=str(stock_data['volume']),
            previous_close_price=str(stock_data['previous_close_price'])
        ))
    print("Closing connection...")
    connection.close()
def generate_id(db):
    # Query the length of the Stock table
    table_length = db.query(func.count(models.Stock.id)).scalar()
    # Generate ID based on the length of the table
    print(table_length)
    return table_length + 1

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


