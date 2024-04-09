from fastapi import FastAPI, HTTPException, Request, status, Depends

from typing import Annotated # to annotate session dependency
from pydantic import BaseModel, Field # only for ORM use? and data validation
import database
from database import engine, SessionLocal, generate_id
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

try:
    database.Base.metadata.create_all(bind=engine)
    print("Creating all tables from models to database")
except Exception as e:
    print("Error: ", e)

############ database dependency
def get_db():
    print("Creating session in get_db()")
    db = SessionLocal()
    db.__init__
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]


# Fetching stock data from StockAPI and returning a list of stocks
def fetch_api_data(db) -> list:
    try:
        stockcodes = ["AAPL,TSLA,MSFT"] #, "KO,NVDA,GOOG", "AMZN,LLY,JPM" <- lisää nämä kun tarvitaan enemmän tietoja
        stock_data_list = []
        for code in stockcodes:
            url = f"https://api.stockdata.org/v1/data/quote?symbols={code}&api_token={TOK_API_TOKEN}"
            response = requests.get(url)

            if response.status_code == 200:
                quotes_data = json.loads(response.text)

                if 'data' in quotes_data:
                    stock_data = quotes_data['data']   
                    # Print out the fetched data
                    print(f"Fetched stock quotes for {len(stock_data)} stocks:")

                    for stock in stock_data:
                        stock_info = {
                            "id": generate_id(db), 
                            "ticker": stock['ticker'],
                            "name": stock['name'],
                            "price": stock['price'],
                            "volume": stock['volume'],
                            "previous_close_price": stock['previous_close_price']
                        }
                        
                        stock_data_list.append(stock_info)
                print(stock_data_list)             
        return stock_data_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

######################    
#FastAPI endpoints  to PORTFOLIO
# Endpoint to populate the database
@app.post("/populate_database")
def populate_database(db: Session = Depends(get_db)):
    try:
        stock_data_list = fetch_api_data(db)
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

app.put("/change_stock")

def pull_table():
    
    
    
    return 
    
    
@app.get("/stock/{stock_id}")
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

app.get("/")