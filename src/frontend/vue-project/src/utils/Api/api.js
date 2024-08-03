// utils/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
