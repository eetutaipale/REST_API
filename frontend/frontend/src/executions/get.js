// api.js

import axios from 'axios';

const apiUrl = 'http://127.0.0.1:8000'; // Replace with your actual backend URL

export const fetchData = async (endpoint) => {
  try {
    const response = await axios.get(`${apiUrl}/${endpoint}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};
// TODO: Write your task or comment here
export const buyStock = async ({ stockId, portfolioId, amount }) => {

  try {
    const response = await fetch(`${apiUrl}/transactions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        stock_id: stockId,
        portfolio_id: portfolioId,
        stock_amount: amount,
      }),
    });
    if (!response.ok) {
      throw new Error('Failed to buy stock');
    }
    return response.json();
  } catch (error) {
    console.error('Error buying stock:', error);
    throw error;
  }
};

export const Updateportfolio = async ({ stockId, portfolioId, amount }) => {

}

export const SellStock = async (transactionId) => {
  try {
    const response = await fetch(`${apiUrl}/transactions/${transactionId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        transaction_id: transactionId,
      }),
    });
    if (!response.ok) {
      throw new Error('Failed to delete transaction');
    }
    return response.json();
  } catch (error) {
    console.error('Error deleting transaction:', error);
    throw error;
  }
};
export const createPortfolio = async (portfolioValue) => {
  
  try {
    
    const response = await fetch(`${apiUrl}/portfolio/post`, {
      
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        portfolio_value: portfolioValue
      }),
    });
    if (!response.ok) {
      throw new Error('Failed to create portfolio');
    }
    return response.json();
  } catch (error) {
    console.error('Error creating portfolio:', error);
    throw error;
  }
};