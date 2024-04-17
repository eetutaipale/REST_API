from fastapi import FastAPI, HTTPException, Request, status, Depends

from typing import Annotated # to annotate session dependency
from pydantic import BaseModel, Field # only for ORM use? and data validation
import database
from database import engine, SessionLocal, get_table_length
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import models

import requests
import json
import os

load_dotenv()

##################
app = FastAPI()
TOK_API_TOKEN = os.getenv("TOK_API_TOKEN")

# This try-clause ought to be better placed
try:
    database.Base.metadata.create_all(bind=engine)
    print("Creating all tables from models to database")
except Exception as e:
    print("Error: ", e)

# Database dependency method
def get_db():
    print("Creating session in get_db()")
    db = SessionLocal()
    db.__init__
    try:
        yield db
    finally:
        db.close()

# Checks the amout of models.Stock -type items in database and returns next value as int
def generate_id(db: Session) -> int:
    # Query the length of the Stock table
    table_length = db.query(models.Stock).count()
    # Generate ID based on the length of the table
    return table_length + 1

db_dependency = Annotated[Session, Depends(get_db)]

# Fetching stock data from StockAPI and returning a list of stocks
def fetch_api_data() -> list:
    try:
        stock_tickers_list = ["AAPL,TSLA,MSFT"] #, "KO,NVDA,GOOG", "AMZN,LLY,JPM" <- lisää nämä kun tarvitaan enemmän tietoja
        stock_data_list = []
        table_length = get_table_length('stock_data')
        print("Length of 'stock_data' table:", table_length)

        for ticker in stock_tickers_list:
            url = f"https://api.stockdata.org/v1/data/quote?symbols={ticker}&api_token={TOK_API_TOKEN}"
            response = requests.get(url)

            if response.status_code == 200:
                quotes_response = json.loads(response.text)

                if 'response' in quotes_response:
                    stock_data = quotes_response['response']   
                    # Print out the fetched data
                    print(f"Fetched stock quotes for {len(stock_data)} stocks:")

                    for stock in stock_data:
                        stock_info = {
                            "id": table_length,
                            "ticker": stock['ticker'],
                            "name": stock['name'],
                            "price_today": stock['price'],
                            "volume": stock['volume'],
                            "last_days_price": stock['previous_close_price']
                        }
                        stock_data_list.append(stock_info)
                        table_length += 1
        return stock_data_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

######################    
# FastAPI endpoints  to PORTFOLIO
# Endpoint to populate the database
@app.post("/populate_database")
def populate_database(db: Session = Depends(get_db)):
    try:
        stock_data_list = fetch_api_data()
        for stock_data in stock_data_list:
            stock = models.Stock(**stock_data) #be sure of stock_data model
            db.add(stock)
        db.commit()
        return {"message": "Tried to populate database with fetch_api_data"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
# Post toimii 
@app.post("/stock_data/")
def create_stock(stock: models.StockBase, db: Session = Depends(get_db)):
    try:
        print("Trying to post("")")
        db_stock = models.Stock(**stock.model_dump())
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        return db_stock
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/stock_data/")
def get_stock(db: Session = Depends(get_db)):
    stock_data = db.query(models.Stock).all()
    if not stock_data:
        raise HTTPException(status_code=404, detail="Stock_data not found")
    return stock_data

@app.get("/stock_data/{stock_id}")
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@app.put("/stocks/{id}/update-volume/")
async def update_volume(id: int, volume: int, db: Session = Depends(get_db)):
    stock = db.query(models.Stock).filter(models.Stock.id == id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock.volume = volume
    db.commit()
    db.refresh(stock)
    return {"message": "Volume updated successfully", "ticker": id, "new_volume": volume}