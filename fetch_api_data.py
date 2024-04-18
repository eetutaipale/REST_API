# Fetching stock data from StockAPI and returning a list of stocks
import datetime
import json
import os
from fastapi import HTTPException
import requests
from database import get_table_length
from dotenv import load_dotenv

load_dotenv()
TOK_API_TOKEN = os.getenv("TOK_API_TOKEN")


def fetch_api_data() -> list:
    print("\nFetching API data form stockapi.org . . . ")
    print("Token for api : ", TOK_API_TOKEN)
    try:
        stock_tickers_list = ["AAPL,TSLA,MSFT"] #, "KO,NVDA,GOOG", "AMZN,LLY,JPM" <- lisää nämä kun tarvitaan enemmän tietoja
        stock_data_list = []
        table_length = get_table_length('stock')
        print("\nLength of 'stock_data' table:", table_length)

        for ticker in stock_tickers_list:
            url = f"https://api.stockdata.org/v1/data/quote?symbols={ticker}&api_token={TOK_API_TOKEN}"
            response = requests.get(url)

            if response.status_code == 200:
                quotes_data = json.loads(response.text)
                print("Response status OK")
                
                if 'data' in quotes_data:
                    stock_data = quotes_data['data']   
                    # Print out the fetched data
                    print(f"Fetched stock quotes for {len(stock_data)} stocks:")
                    today = datetime.date.today()
                    if type(today) == str:
                        pass
                    else:
                        today = today.strftime('%Y-%m-%d')
                for stock in stock_data:
                        
                        stock_info = {
                            "id": table_length,
                            "ticker": stock['ticker'],
                            "name": stock['name'],
                            "price_today": stock['price'],
                            "volume": stock['volume'],
                            "last_days_price": stock['previous_close_price'],
                            "date": today
                        }
                        stock_data_list.append(stock_info)
                        table_length += 1  
        return stock_data_list
    except Exception as e:
        print("Fetching from stockdata API failed.")
        raise HTTPException(status_code=500, detail=str(e))