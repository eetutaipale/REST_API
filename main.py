import json
from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

TOK_API_TOKEN = os.getenv("TOK_API_TOKEN")
def get_and_print_stock_quotes():
    try:
        stockcodes = ["AAPL,TSLA,MSFT"] #, "KO,NVDA,GOOG", "AMZN,LLY,JPM" <- lisää nämä kun tarvitaan enemmän tietoja
        stock_info_list = []
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
                            "ticker": stock['ticker'],
                            "name": stock['name'],
                            "price": stock['price'],
                            "volume": stock['volume'],
                            "previous_close_price": stock['previous_close_price']
                        }
                        stock_info_list.append(stock_info)
            
            
        return stock_info_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#print(get_and_print_stock_quotes())
@app.get("/another")
async def root():
    return {"message": "Another one!"}

@app.get("/get_stock_quotes")
async def quotes():
    stock = get_and_print_stock_quotes()
    return {"stock data": stock}
