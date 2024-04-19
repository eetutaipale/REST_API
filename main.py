
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


# Creates an id by checking the amout of models.Stock -type items in database and returns next value as int
def generate_id(db: Session) -> int:
    table_length = db.query(models.Stock).count()
    return table_length + 1

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
        return {"added stockdata"}

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

# Endpoint to READ stock by stock_id number
@app.get("/stock/{stock_id}")
async def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

# Endpoint to UPDATE a certain stock data 
# TODO: UPDATE stock amount by certain id, currently updating in path /stock/ but maybe needs to be fixed and 
@app.put("/stock/{id}/update-volume/")
async def update_volume(id: int, volume: int, db: Session = Depends(get_db)):
    stock = db.query(models.Stock).filter(models.Stock.id == id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock.volume = stock.volume + volume 
    print("Added a sum here -stock.volume + volume-, might cause an error. ") 
    db.commit()
    db.refresh(stock)
    return {"message": "Volume updated successfully", "ticker": id, "new_volume": volume}

# Endpoint to READ a portfolio and it's contents (stocks it holds)
@app.get("/portfolios/")
async def get_portfolios(db: Session = Depends(get_db)): 
    portfolios = db.query(models.Portfolio).all()
    return portfolios

# Endpoint to CREATE a transaction 
# TODO: should make a transaction with transaction_id referring to portfolio_id and stock_id

# Endpoint to UPDATE porfolio_item with an id
# TODO: This should probably be a CREATE method as app.post?
@app.put("/portfolio/{id}")
async def update_portfolio_item(portfolio_id: int, portfolio_value: int, db: Session = Depends(get_db)):
    portfolio_item = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if portfolio_item:
        portfolio_item.portfolio_value = portfolio_value
        db.commit()
        return portfolio_item
    else:
        raise HTTPException(status_code=404, detail="Portfolio item not found")

# Endpoint to CREATE a portfolio    
@app.post("/portfolio/")
async def create_portfolio(portfolio: models.PortfolioBase, db: Session = Depends(get_db)):
    db_portfolio = models.Portfolio(**portfolio.model_dump())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

# Endpoint to DELETE a certain stock from portfolio
@app.delete("/portfolio/{id}")
async def delete_portfolio_item(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio_item = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if portfolio_item:
        db.delete(portfolio_item)
        db.commit()
        db.refresh(portfolio_id)

        return {"message": "Portfolio item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
# Endpoint to CREATE a transaction, does not need a PUT or DELETE in my opinion
# TODO: Should add a transaction by id into database, no database calls for now here
@app.post("/transactions/", operation_id="create_transaction")
async def create_transaction(stock_id: int, portfolio_id: int, stock_amount: int, db: Session = Depends(get_db)):
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

# @app.post("/transactions/" )
# async def create_transaction(transaction: models.TransactionCreate,  # Assuming the date is passed as a string // TODO: This might cause an error 
#         db: Session = Depends(get_db)
#         ):
#     # Check if portfolio and stock exist
#     portfolio = db.query(models.Portfolio).get(Portfolio.portfolio_id)
#     stock = db.query(models.Stock).get(stock_id)

#     if not portfolio:
#         raise HTTPException(status_code=404, detail="Portfolio not found")
#     if not stock:
#         raise HTTPException(status_code=404, detail="Stock not found")
#     today = datetime.date.today()
#     new_transaction= models.Transaction(
#         stock_id=stock_id,
#         portfolio_id=portfolio_id,
#         stock_amount=stock_amount,
#         purchase_date=today,
#     )
#     db.add(new_transaction)
#     db.commit()
#     db.refresh(new_transaction)
#     return print(f"Transaction created with Portfolio item: {models.Portfolio(new_transaction)}") 

