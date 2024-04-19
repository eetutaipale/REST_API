
import { fetchData } from './get';
export const findStockNameById = (stockId, exchangeData) => {
    const stock = exchangeData.find(stock => stock.id === stockId);
    return stock ? stock.name : 'Stock Not Found';
  };

