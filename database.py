import logging
from typing import Self
from sqlalchemy import URL, Column, Inspector, create_engine, Table, func, select, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


# Log in credentials and connection URL-string as DATABASE_CONNECTION
load_dotenv()
host1 = "sqlstockserver.database.windows.net"
host2 = "sqlserverest.database.windows.net"
# DATABASE_CONNECTION = f"mssql+pyodbc://{UID}:{PWD}@{SERVER_IP}/{DATABASE}?driver={DRIVER}"
password = os.getenv("password")
engine_str = URL.create(
    drivername="mssql+pyodbc",
    username="meklari",
    password=f"{password}",
    host=f"{host1}",
    port=1433,
    database="Stockdb",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "TrustServerCertificate": "no",
        "Connection Timeout": "30",
        "Encrypt": "yes",
    }
)

# Engine and sessionmaker
engine = create_engine(engine_str, echo=True) # Creating an engine object to connect to database
metadata = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base and making a table to database.
Base = declarative_base()
try:
    inspector = inspect(engine)
    if not inspector.has_table("stock"): # Logic works properly now in with inspector=inspect(engine)
        Base.metadata.create_all(bind=engine) # Create the table if it doesn't exist
        print("Table 'stock_data' created from database.py")
    else:
        print("Table \"stock_data\" exists, not creating new.")

except Exception as e:
    print("Error: ", e)




# Populate database with stockdata
# def populate_database(stock_data_list):
#     print("Save to database in action...")
#     # Set up logging configuration
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s - %(levelname)s - %(message)s',
#                         filename='database.log',
#                         filemode='a')

#     # Using the engine object for straight connection to DB
#     connection = engine.connect()
#     # print(f"Conncetion opened to {DATABASE} @ {SERVER_IP}")
#     stock_data_table = Table('stock_data', metadata,
#         Column('id', int, primary_key=True),
#         Column('name', str),
#         Column('price', str),
#         Column('volume', str),
#         Column('previous_close_price', str)

#     )
#     # SQL query with SQLAlchemy methods
#     if not metadata.tables.get('stock_data'):
#         # Create the table if it doesn't exist
#         stock_data_table = metadata.create_all()
#         print("Table 'stock_data' created from save_to_database")

#     for stock_data in stock_data_list:
#         connection.execute(stock_data_table.insert().values(
#             name=stock_data['name'],
#             price=str(stock_data['price']),
#             volume=str(stock_data['volume']),
#             previous_close_price=str(stock_data['previous_close_price'])
#         ))
#     print("Closing connection...")
#     connection.close()

# def create_portfolio_item(session, stocks: str, value: int):
#     new_portfolio_item = Portfolio(stocks=stocks, value=value)
#     session.add(new_portfolio_item)
#     session.commit()
#     return new_portfolio_item

# # READ function, read portfolio
# def get_portfolio(session):
#     return session.query(Portfolio).all()


# # UPDATE function, update existing portfolio item
# def update_portfolio_item(session, portfolio_id: int, stocks: str, value: int):
#     portfolio_item = session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
#     if portfolio_item:
#         portfolio_item.stocks = stocks
#         portfolio_item.value = value
#         session.commit()
#         return portfolio_item
#     else:
#         return None  # Portfolio item not found

# # DELETE function, delete from portfolio
# def delete_portfolio_item(session, portfolio_id: int):
#     portfolio_item = session.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
#     if portfolio_item:
#         session.delete(portfolio_item)
#         session.commit()
#         return True
#     else:
#         return False  # Portfolio item not found

def get_table_length(table_name):
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    with engine.connect() as connection:
        result = connection.execute(func.count().select().select_from(table))
        table_length = result.scalar()
        return table_length + 1
