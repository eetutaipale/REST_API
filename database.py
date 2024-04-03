
from sqlalchemy import Column, create_engine, Table, select, MetaData
from dotenv import load_dotenv
import os
# from sqlalchemy.orm import sessionmaker -> when taking ORM into use, use sessions
import time
import logging

#import pandas as pd
def save_to_database(stock_data_list):
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
        stock_data_table.create()
        print("Table 'stock_data' created")

        for stock_data in stock_data_list:
            stock_data_table.insert().values(
                name=stock_data['name'],
                price=str(stock_data['price']),
                volume=str(stock_data['volume']),
                previous_close_price=str(stock_data['previous_close_price'])
            ).execute()
        

    time.sleep(1)

    print("Closing connection...")
    connection.close()



