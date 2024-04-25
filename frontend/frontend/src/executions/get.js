// api.js

import axios from 'axios';


const apiUrl = 'http://127.0.0.1:8000'; // Replace with your actual backend URL

// Function to fetch data from an endpoint
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

// Function to sell stock 
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

// Function to create a portfolio
export const createPortfolio = async (portfolioValue) => {
  try {  
    const response = await fetch(`${apiUrl}/portfolios/post`, {
      
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

export const updatePortfolio = async ({ portfolioId, newValue }) => {
  try {
    const response = await fetch(`${apiUrl}/portfolios/${portfolioId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        portfolio_id: portfolioId,
        portfolio_value: newValue,
      }),
    });
    // Check if response status is in the 2xx range
    if (response.status >= 200 && response.status < 300) {
      return response.json(); // Return response data if successful
    } else {
      throw new Error('Failed to update portfolio value'); // Throw error if unsuccessful
    }

  } catch (error) {
    console.error('Error updating portfolio value:', error);
    throw error;
  }
}