
from sqlalchemy import create_engine, Table, select, MetaData
from dotenv import load_dotenv
import os
# from sqlalchemy.orm import sessionmaker -> when taking ORM into use, use sessions
import time
import logging

#import pandas as pd

load_dotenv()
metadata = MetaData()

# Log in credentials and connection URL-string as DATABASE_CONNECTION
SERVER_IP = os.getenv("SERVER_IP")
DRIVER = os.getenv("DRIVER")
DATABASE = os.getenv("DATABASE")
UID = os.getenv("UID")
PWD = os.getenv("PWD")
DATABASE_CONNECTION = f"mssql+pyodbc://{UID}:{PWD}@{SERVER_IP}/{DATABASE}?driver={DRIVER}"

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='database.log',
                    filemode='a')

# Creating an engine object to connect to database
engine = create_engine(DATABASE_CONNECTION)

# Using the engine object for straight connection to DB
connection = engine.connect()
print(f"Conncetion opened to {DATABASE} @ {SERVER_IP}")

# SQL query with SQLAlchemy methods
try:
    result = connection.execute(select(Table('test_data', metadata, autoload_with=engine)))

    rows = result.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    logging.error("An error occurred: ", exc_info=True)
    print("Error:", e)
time.sleep(1)

print("Closing connection...")
connection.close()

