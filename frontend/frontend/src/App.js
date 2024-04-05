import React, { useState } from 'react';
import './App.css';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
// Icon Imports
import { SiApple, SiTesla, SiNvidia, SiMicrosoft, SiAmazon, SiGoogle, SiCocacola } from "react-icons/si";

// Custom Row Component for My Stocks Page
const MyStockRow = ({ icon, name, change, value, volume }) => {
  // Determine the class for the value based on the change
  const valueClass = change.includes('+') ? 'positive' : 'negative';

  return (
    <div className="excel-row">
      <div className="excel-cell">
        <div className="icon">{icon}</div>
        <div className="name">{name}</div>
      </div>
      <div className={`excel-cell ${valueClass}`}>{change}</div>
      <div className="excel-cell">{value}</div>
      <div className="excel-cell">{volume}</div>
    </div>
  );
};

// Custom Row Component for Exchange Page
const StockRow = ({ icon, name, change, value }) => {
  // Determine the class for the value based on the change
  const valueClass = change.includes('+') ? 'positive' : 'negative';

  return (
    <div className="excel-row">
      <div className="excel-cell">
        <div className="icon">{icon}</div>
        <div className="name">{name}</div>
      </div>
      <div className={`excel-cell ${valueClass}`}>{change}</div>
      <div className="excel-cell">{value}</div>
    </div>
  );
};

function App() {
  const [currentPage, setCurrentPage] = useState('myStocks');

  const changePage = (page) => {
    setCurrentPage(page);
  };

  // Uncomment the following code when implementing data fetching from backend
  /*
  const [stocksData, setStocksData] = useState([]);

  useEffect(() => {
    // Fetch data from the backend
    fetch('http://your-backend-url/api/stocks')
      .then(response => response.json())
      .then(data => {
        setStocksData(data); // Update stocks data state with fetched data
      })
      .catch(error => console.error('Error fetching stocks data:', error));
  }, []); // Empty dependency array to ensure useEffect only runs once
  */

  const renderPage = () => {
    if (currentPage === 'exchangeRates') {
      return (
        <Container>
          <Typography variant="h4">Stocks</Typography>
          <div className="excel-table">
            <div className="excel-row header">
              <div className="excel-cell">Name</div>
              <div className="excel-cell">Daily Change</div>
              <div className="excel-cell">Value</div>
            </div>
      
            {/* 
            {stocksData.map(stock => (
              <StockRow
                key={stock.id}
                icon={<img src={stock.iconUrl} alt={stock.name} />} // Assuming the backend returns the icon URL
                name={stock.name}
                change={stock.dailyChange}
                value={stock.value}
              />
            ))}
            */}
            <StockRow icon={<SiApple size={24} />} name="Apple" change="+2.5%" value="$150" />
            <StockRow icon={<SiTesla size={24} />} name="Tesla" change="+3.2%" value="$700" />
            <StockRow icon={<SiNvidia size={24} />} name="Nvidia" change="+1.8%" value="$300" />
            <StockRow icon={<SiMicrosoft size={24} />} name="Microsoft" change="+1.0%" value="$250" />
            <StockRow icon={<SiAmazon size={24} />} name="Amazon" change="+2.7%" value="$3300" />
            <StockRow icon={<SiGoogle size={24} />} name="Google" change="+1.5%" value="$2800" />
            <StockRow icon={<SiCocacola size={24} />} name="Coca-Cola" change="-0.3%" value="$50" />
          </div>
        </Container>
      );
    } else if (currentPage === 'myStocks') {
      // Mock user's stocks data
      const userStocks = [
        { icon: <SiApple size={24} />, name: "Apple", change: "+2.5%", value: "$150", volume: 10 },
        { icon: <SiNvidia size={24} />, name: "Nvidia", change: "+1.8%", value: "$300", volume: 15 },
        { icon: <SiGoogle size={24} />, name: "Google", change: "+1.5%", value: "$2800", volume: 5 }
      ];

      return (
        <Container>
          <Typography variant="h4">My Stocks</Typography>
          <div className="excel-table">
            <div className="excel-row header">
              <div className="excel-cell">Name</div>
              <div className="excel-cell">Daily Change</div>
              <div className="excel-cell">Value</div>
              <div className="excel-cell">Volume</div>
            </div>
            {userStocks.map((stock, index) => (
              <MyStockRow key={index} {...stock} />
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
