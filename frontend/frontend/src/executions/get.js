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