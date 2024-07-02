// utils/csrf.js
import axios from "axios";
import Cookies from 'js-cookie';

// Function to check if CSRF cookie is valid
async function checkCSRF() {
  try {
    const response = await axios.get("/api/csrf-token/check");
    if (response.data.status === "off") {
      console.log("CSRF token is invalid or expired");
      Cookies.remove('csrf_token');
      return false;
    }
    return true;
  } catch (error) {
    console.error("Error checking CSRF token:", error);
    return false;
  }
}

// Function to fetch and set CSRF token
export default async function fetchAndSetCsrfToken() {
  try {
    const status = await checkCSRF();
    if (status) {
      console.log('Valid CSRF tokens were found');
      return; // CSRF token is valid, no need to fetch a new one
    }
    console.log('No valid CSRF tokens were found');

    // Fetch new CSRF token from the server
    const response = await axios.post("/api/csrf-token");
    axios.defaults.headers.common['X-CSRFToken'] = response.data.csrf_token;
    localStorage.setItem('auth-token', response.data.csrf_token);
  } catch (error) {
    console.error("Error fetching CSRF token:", error);
    throw error;
  }
}
