
from urllib import request
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated 
from database import create_all_tables, engine, SessionLocal, get_table_length, get_db
from fetch_api_data import fetch_api_data
from dotenv import load_dotenv

import datetime
import models
import datetime

# Todos overall
# TODO: Investigate if db.refresh() is needed after endpoint function calls

# Middleware function to setup compatibility with frontend
def setup_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Add the origin of your frontend
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

# Setup functions for the App
app = FastAPI()
db_dependency = Annotated[Session, Depends(get_db)]
load_dotenv()
setup_middleware(app)
create_all_tables([models.Stock, 
                   models.Portfolio, 
                   models.Transaction])

######################    
# FastAPI ENDPOINTS to communicate with client/frontend
# TODO: Function should populate the data once a day automatically if running -- let's see if this is needed
@app.post("/populate_database")
async def populate_database(db: Session = Depends(get_db)):
    try:
        stock_data_list = fetch_api_data()
        for stock_data in stock_data_list:
            stock = models.Stock(**stock_data) #be sure of stock_data model
            db.add(stock)
        db.commit()
        return stock_data_list

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to CREATE new stock, only used for test purposes
@app.post("/stock/")
async def create_stock(stock: models.StockCreate, db: Session = Depends(get_db)):
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
    
# Endpoint to READ data all data from /stock/
@app.get("/stock/")
async def get_stock(db: Session = Depends(get_db)):
    today = datetime.date.today()
    print(today)
    stock_data = db.query(models.Stock).all()
    if not stock_data:
        raise HTTPException(status_code=404, detail="Stock_data not found")
    return stock_data

# Endpoint to READ stock by stock_id number TODO: Not necessary
@app.get("/stock/{stock_id}")
async def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

# Endpoint to CREATE a portfolio    
@app.post("/portfolios/")
async def create_portfolio(portfolio: models.PortfolioBase, db: Session = Depends(get_db)):
    db_portfolio = models.Portfolio(**portfolio.model_dump())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

# Endpoint to READ a portfolio and it's contents (stocks it holds)
@app.get("/portfolios/")
async def get_portfolios(db: Session = Depends(get_db)): 
    portfolios = db.query(models.Portfolio).all()
    return portfolios

# Endpoint to READ portfolio by ID 
@app.get("/portfolios/{id}") 
async def get_portfolio(id: int, db: Session = Depends(get_db)):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == id).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

# TODO: This should probably be used in changing portfolio.value
@app.put("/portfolios/{id}")
async def update_portfolio_item(request_data: dict, db: Session = Depends(get_db)):
    portfolio_id = request_data.get('portfolio_id')
    portfolio_value = request_data.get('portfolio_value')

    portfolio_item = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if portfolio_item:
        portfolio_item.portfolio_value = portfolio_value
        db.commit()
        return portfolio_item
    else:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
# Endpoint to DELETE a certain portfolio
@app.delete("/portfolios/{id}")
async def delete_portfolio_item(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio_item = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if portfolio_item:
        db.delete(portfolio_item)
        db.commit()
        db.refresh(portfolio_id)

        return {"message": "Portfolio item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
# Endpoint to CREATE a transaction
@app.post("/transactions/")
async def create_transaction(request_data: dict, db: Session = Depends(get_db)):
    # Extract data from request body
    stock_id = request_data.get('stock_id')
    portfolio_id = request_data.get('portfolio_id')
    stock_amount = request_data.get('stock_amount')

    # Check if stock and portfolio exist
    stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    today = datetime.date.today()
    # Create a new transaction
    new_transaction = models.Transaction(stock_id=stock_id, portfolio_id=portfolio_id, stock_amount=stock_amount, purchase_date=today)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction
# Endpoint to READ transaction data. 
@app.get("/transactions/")
async def get_transactions(db: Session = Depends(get_db)):
    try:
        transactions = db.query(models.Transaction).all()
        return transactions
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Transaction data not found, {e}")

# Endpoint to READ transaction by ID 
@app.get("/transactions/{id}") 
async def get_transaction(id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == id).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# Enpoint DELETES a tranaction by ID number. 
@app.delete("/transactions/{id}") #taitaa toimia
async def delete_transaction_item(request_data: dict, db: Session = Depends(get_db)):
    transaction_id = request_data.get('transaction_id')
    transaction_item = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if transaction_item:
        db.delete(transaction_item)
        db.commit()
        #db.refresh(transaction_item)
        return {"message": "Transaction item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Transaction item not found")
    
# TODO: transaktioiden osto ja myynti toiminto järkevästi -> tyyppi buy sell tai transaktioiden mukaan myynti.  
# TODO: Tulee poistaa kaikki transactiot, jotka liittyy kyseiseen portfolioon

