import logging
from typing import Self
from sqlalchemy import URL, Column, Inspector, create_engine, Table, func, select, MetaData, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Logging and other relevant configuration
load_dotenv()
Base = declarative_base()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection parameters
host1 = "sqlstockserver.database.windows.net"
host2 = "sqlserverest.database.windows.net" # Old server

# Connection parameters with SQL server local version
database_name = "Stockdb"
server_local = os.getenv("serverlocal")
print(server_local)
string_local = f"mssql+pyodbc://@{server_local}/{database_name}?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server"
print(string_local)
# Connection string for SQL Server with Azure cloud SQL
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

# Engine and sessionmaker // When making cloud based, remember to change connection string
engine = create_engine(string_local, echo=True) # Creating an engine object to connect to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Method to inspecting tables in database before creating new 
def create_all_tables(tables: list):
    try:
        print("Checking database tables, and creating all non existing tables.")
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        tables_to_create = []

        for table in tables:
            if table.__tablename__ not in existing_tables:
                print(f"Table {table.__tablename__} does not exist - Creating it.")
                tables_to_create.append(table)
                print(tables)
                print(tables_to_create)

        if tables_to_create:
            print(f"Trying to create {table}.")
            Base.metadata.create_all(engine) #, tables=tables_to_create
            print(f"{table} created successfully.")
        else:
            print("All tables exist.")

    except Exception as e:
        print("Error from create_all_tables:", e, e.args)


# Get lentgh of the table in database for id creation
def get_table_length(table_name):
    try:
        metadata.reflect(bind=engine)
        table = metadata.tables[table_name]
        with engine.connect() as connection:
            result = connection.execute(func.count().select().select_from(table))
            table_length = result.scalar()
            return table_length + 1
    except SQLAlchemyError as e:
        logger.error(f"Error while getting table length: {e}")

# Database dependency method to start a db_session
def get_db():
    print("Creating session in get_db()")
    db = SessionLocal()
    db.__init__
    try:
        yield db
    finally:
        db.close()