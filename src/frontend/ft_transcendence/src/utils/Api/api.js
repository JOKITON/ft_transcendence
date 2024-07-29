// utils/api.js
import axios from 'axios';
import Cookies from 'js-cookie';

const api = axios.create({
  baseURL: 'http://localhost/api/',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export default api;
