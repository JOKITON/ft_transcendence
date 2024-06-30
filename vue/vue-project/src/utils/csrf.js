// src/utils/csrf.js
import axios from "axios";

export default async function fetchCsrfToken() {
  try {
    const response = await axios.get('/api/csrf-token');
    return response.data.csrfToken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    throw error;
  }
}
