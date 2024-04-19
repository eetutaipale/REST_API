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
import { fetchData, buyStock, createPortfolio } from './executions/get';  
// Custom Row Component for My Stocks Page
const MyStockRow = ({ stockId, stock_amount, purchase_date, exchangeData }) => {
  const stockName = findStockNameById(stockId, exchangeData);
  return (
    <div className="excel-row">
      <div className="excel-cell">
        <div className="name">{stockName}</div>
      </div>
      <div className="excel-cell">{stock_amount}</div>
      <div className="excel-cell">{purchase_date}</div>
    </div>
  );
};

// Custom Row Component for Exchange Page
const StockRow = ({icon, name, change, value, onBuy }) => {
  const valueClass = change.includes('-') ? 'negative' : 'positive';

  return (
    <div className="excel-row">
      <div className="excel-cell">
        <div className="icon">{icon}</div>
        <div className="name">{name}</div>
      </div>
      <div className={`excel-cell ${valueClass}`}>{change}</div>
      <div className="excel-cell">{value}</div>
      <div className="excel-cell">
        <button onClick={onBuy}>Buy</button>
      </div>
    </div>
  );
};
const LatestStocks = ({ stocks }) => {
  // Find the most recent date
  const mostRecentDate = stocks.reduce((maxDate, stock) => {
    return stock.date > maxDate ? stock.date : maxDate;
  }, '');

  // Filter stocks for the most recent date
  const latestStocks = stocks.filter(stock => stock.date === mostRecentDate);

  return (
    <div>
      {latestStocks.map(stock => (
        <StockRow
          key={stock.id}
          icon={getIconByTicker(stock.ticker)}
          name={stock.name}
          change={`$${((stock.price_today - stock.last_days_price) / stock.last_days_price * 100).toFixed(3)}%`}
          value={`$${stock.price_today}`}
          onBuy={() => console.log('Buy button clicked for', stock.name)}
        />
      ))}
    </div>
  );
};

function App() {
  const [currentPage, setCurrentPage] = useState('myStocks');
  const [exchangeData, setExchangeData] = useState([]);
  const [myStocks, setMyStocks] = useState([]);
  const [portfolioId, setPortfolioId] = useState(null);
  const [transactionData, settra] = useState([]);
  const changePage = (page) => {
    setCurrentPage(page);
  };
  


  
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const exchangeResponse = await fetchData('stock/'); // Fetch exchange data
        console.log(exchangeResponse);
        setExchangeData(exchangeResponse);

        const transactionresponse = await fetchData('transactions/'); // Fetch exchange data
        console.log(transactionresponse);
        settra(transactionresponse);

        const myStocksResponse = await fetchData('portfolios/'); // Fetch user's stocks
        console.log(myStocksResponse);
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
              <div className="excel-cell">Purchase date</div>
              
            </div>
            {transactionData.map((transaction) => (
              <MyStockRow
              key={transaction.id}
              stockId={transaction.stock_id}
              stock_amount={transaction.stock_amount}
              purchase_date={transaction.purchase_date}
              exchangeData={exchangeData}
              
            />
            ))}
          </div>
        </Container>
      );
    } 
  };

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