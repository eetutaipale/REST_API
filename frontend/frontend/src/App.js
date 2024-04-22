import React, { useState, useEffect } from 'react';
import './App.css';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { findStockNameById } from './executions/stockUtils';
import { getIconByTicker } from './executions/logos';
import { fetchData, buyStock, createPortfolio, SellStock, Updateportfolio } from './executions/get';  
import Notification from './executions/Notification'





// Function component to handle the application logic
function App() {
  // State variables
  const [currentPage, setCurrentPage] = useState('exchangeRates');
  const [exchangeData, setExchangeData] = useState([]);
  const [myStocks, setMyStocks] = useState([]);
  const [portfolioId, setPortfolioId] = useState(null);
  const [transactionData, setTransactiondata] = useState([]);
  const [portfolioName, setPortfolioName] = useState('');
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  
  const [errorMessage, setErrorMessage] = useState(null)
  const [validMessage, setMessage] = useState(null)


  // Fetch initial data when the component mounts
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const exchangeResponse = await fetchData('stock/'); // Fetch exchange data
        
        setExchangeData(exchangeResponse);

        const transactionresponse = await fetchData('transactions/'); // Fetch exchange data
        
        setTransactiondata(transactionresponse);

        const myStocksResponse = await fetchData('portfolios/'); // Fetch user's stocks
        
        setMyStocks(myStocksResponse);


        // Fetch or create user's portfolio and get the ID
        const portfolioResponse = await fetchData('portfolios/');
        if (portfolioResponse.length > 0) {
          setPortfolioId(portfolioResponse[0].id);
        } else {
          const newPortfolioResponse = await createPortfolio(1000); // Initial portfolio value: $1000
          setPortfolioId(newPortfolioResponse.id);
        }
      } catch (error) {
        console.error('Error fetching initial data:', error);
      }
    };

    fetchInitialData();
  }, []);
  // changes the current transactions when you buy or sell a stock by calling handleSeacrch
  useEffect(() => {
    if (transactionData.length > 0) {
      handleSearch();
    }
  }, [transactionData]);
  // Function to handle portfolio name change
  const handlePortfolioChange = (e) => {
    setPortfolioName(e.target.value);
  };

  // function that handles portfolios changes based in input and shows an error meassage if portfolio is not found
  const handleSearch = () => {
    try {
      findPortfolioIdByName(portfolioName);
      setErrorMessage('')
    } catch (error) {
      setErrorMessage("Porfolio not found")
      setFilteredTransactions([])
      
    }
  };

  // Function to change the current page
  const changePage = (page) => {
    setCurrentPage(page);
  };
  // Function to that calculates one transactions profit based on todays price
  const Valuecalculator = (OneTransactions, exchangeData) => {
  
    const mostRecentDate = exchangeData.reduce((maxDate, stock) => {
      return stock.date > maxDate ? stock.date : maxDate;
    }, '');
    
    const latestStocks = exchangeData.filter(stock => stock.date === mostRecentDate);
    const stock = exchangeData.find(stock => stock.id === OneTransactions.stock_id);
    const stockOnPurchaseName = latestStocks.find(name => name.name === stock.name) 
    
    return stockOnPurchaseName.price_today - stock.price_today
    }

  // Function to find portfolio ID by name and searhes the right transactions based on the user
  const findPortfolioIdByName = (portfolioName) => {
    
    const portfolio = myStocks.find(portfolio => portfolio.portfolio_name === portfolioName);
    setPortfolioId(portfolio.id)
    const filtered = transactionData.filter(transaction => transaction.portfolio_id === portfolio.id);
    setFilteredTransactions(filtered);
  };
  // Function to that calculates total profit of the users portfolio
  const Totalvalue = (portfolioId, filteredTransactions, exchangeData) => {
    let totalStockPrice = 0;


    const mostRecentDate = exchangeData.reduce((maxDate, stock) => {
      return stock.date > maxDate ? stock.date : maxDate;
    }, '');

    const latestStocks = exchangeData.filter(stock => stock.date === mostRecentDate);
    filteredTransactions.forEach(transaction => {
      const stock = exchangeData.find(stock => stock.id === transaction.stock_id);
      if (stock) {
        const stockOnPurchaseDate = latestStocks.find(name => name.name === stock.name);
        if (stockOnPurchaseDate) {
          totalStockPrice += stockOnPurchaseDate.price_today - stock.price_today;
        }
      }
      
    })
    return totalStockPrice
  }
    
  // Custom Row Component for Exchange Page
  const StockRow = ({ icon, name, change, value, onBuy }) => {
    const [buyAmount, setBuyAmount] = useState('');
  
    const valueClass = change.includes('-') ? 'negative' : 'positive';
  
    const handleBuy = () => {
      // Call the onBuy callback with the current buyAmount value
      onBuy(buyAmount);
      // Clear the buyAmount state after buying
      setBuyAmount('');
    };
  
    return (
      <div className="excel-row">
        <div className="excel-cell">
          <div className="icon">{icon}</div>
          <div className="name">{name}</div>
        </div>
        <div className={`excel-cell ${valueClass}`}>{change}</div>
        <div className="excel-cell">{value}</div>
        <div className="excel-cell">
          <input  
            type="text" 
            value={buyAmount} 
            placeholder="Amount" 
            onChange={({ target }) => setBuyAmount(target.value)}
          />
          <button onClick={handleBuy}>Buy</button>
        </div>
      </div>
    );
  };
  
  // Custom Row Component for My Stocks Page
  const MyStockRow = ({ stockId, stock_amount, purchase_date, exchangeData, SellStock, value, id}) => {
    const stockName = findStockNameById(stockId, exchangeData);
    const valueClass = value.includes('-') ? 'negative' : 'positive';
    return (
      <div className="excel-row">
        <div className="excel-cell">
          <div className="name">{stockName}</div>
        </div>
        <div className="excel-cell">{stock_amount}</div>
        <div className={`excel-cell ${valueClass}`}>{value}</div>
        <div className="excel-cell">{purchase_date}</div>
        <div className="excel-cell">
        <button onClick={SellStock}>Sell</button>
    </div>
      </div>
    );
  };
  // Function to handle selling stocks
  const SellStocks = async (transactionId, name) => {
    console.log("onnistui")
    try {
      await SellStock(transactionId);
      // Fetch updated transaction data after selling stock
      const updatedTransactionData = await fetchData('transactions/');
       setTransactiondata(updatedTransactionData);
       
    } catch (error) {
      console.error('Error selling stock:', error);
      throw error;
    }
  };

  // Function to handle buying stocks
  const BuyStocks = async ({ stockId: stockId, amount: amount }) => {
    try {
      if (amount != null && amount > 0 ){
        console.log(portfolioId)
        await buyStock({ stockId: stockId, portfolioId: portfolioId, amount: amount })
        // Fetch updated transaction data after buying stock
        const updatedTransactionData = await fetchData('transactions/');
        setTransactiondata(updatedTransactionData);
        handleSearch()
      } else {
        setErrorMessage("Amount input invalid.");
        <Notification message={errorMessage}/>
        setErrorMessage(null);
        
      }

    } catch (error) {
      console.error('Error buying stock:', error);

    }
  };

  // Component to display latest stock data
  const LatestStocks = ( {stocks}, portfolioId ) => {
    // Find the most recent date
    const mostRecentDate = stocks.reduce((maxDate, stock) => {
      return stock.date > maxDate ? stock.date : maxDate;
    }, '');
  
    // Filter stocks for the most recent date
    const latestStocks = stocks.filter(stock => stock.date === mostRecentDate);
  
    return (
      <div>
        {latestStocks.map(stock => 
          <StockRow
            key={stock.id}
            icon={getIconByTicker(stock.ticker)} 
            name={stock.name}
            change={`$${((stock.price_today - stock.last_days_price) / stock.last_days_price * 100).toFixed(2)}%`}
            value={`$${stock.price_today.toFixed(2)}`}
            onBuy={(amount) => { BuyStocks({ stockId: stock.id, portfolioId: portfolioId, amount: amount }); 
                  
                  console.log('Buy button clicked for', stock.name);  
                }}
          />
        )}
      </div>
    );
  };
  
  // Function to render the appropriate page content
  const renderPage = () => {
    if (currentPage === 'exchangeRates') {
      return (
        <Container>
          <Typography variant="h4">Exchange Rates</Typography>
          <div className="excel-table">
            <div className="excel-row header">
              <div className="excel-cell">Name</div>
              <div className="excel-cell">Daily Change</div>
              <div className="excel-cell">Value</div>
              <div className="excel-cell">Actions</div>
            </div>
            
            <LatestStocks stocks={exchangeData} />
          </div>
        </Container>
      );
    } else if (currentPage === 'myStocks') {
      return (
        <Container>
        <Typography variant="h4">My Stocks</Typography>
        <div className="excel-table">
          <div className="excel-row header">
            <div className="excel-cell">Name</div>
            <div className="excel-cell">Stock amount</div>
            <div className="excel-cell">Profit</div>
            <div className="excel-cell">Purchase date</div>
            <div className="excel-cell">Actions</div>
          </div>
          <div>
          <input type="text" value={portfolioName} onChange={handlePortfolioChange} placeholder="Enter Portfolio Name" />
          <button onClick={ handleSearch}>Search</button>
          {errorMessage && <div className="error"> {errorMessage} </div>}
          </div>
          {filteredTransactions.map((transaction) => (
            <MyStockRow
              key={transaction.id}
              stockId={transaction.stock_id}
              stock_amount={transaction.stock_amount}
              purchase_date={transaction.purchase_date}
              exchangeData ={exchangeData}
              SellStock={() => SellStocks(transaction.id, portfolioId )}
              value={`$${Valuecalculator(transaction, exchangeData)}`}
              
            />
          ))}
        </div>
        <div>
        <div className="excel-cell">Total Profit: {Totalvalue(portfolioId, filteredTransactions, exchangeData)}</div>
        </div>
      </Container>
      );
    } 
  };
  // Render the main application content
  return (
    <div className="App">
      <AppBar position="static">
      </AppBar>
      <Drawer variant="permanent">
        <List>
          <ListItem button onClick={() => changePage('myStocks')}>
          <ListItemText primary="My Stocks" />
          </ListItem>
          <ListItem button onClick={() => changePage('exchangeRates')}>
            <ListItemText primary="Exchange Rates" />
          </ListItem>
        </List>
      </Drawer>
      <main>
        {renderPage()}
      </main>
    </div>
  );
}

export default App;