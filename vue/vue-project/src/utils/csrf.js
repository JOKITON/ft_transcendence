// utils/csrf.js
import axios from "axios";
import Cookies from 'js-cookie';

// Helper function to get a cookie by name
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Function to check if CSRF cookie is valid
async function checkCSRF() {
  const csrfToken = axios.defaults.headers.common['X-CSRFToken'] || getCookie('csrftoken');
  console.log('CSRF Token:', csrfToken);
  
  if (csrfToken) {
      try {
          const response = await axios.get("/api/csrf-token/check");
          if (response.data.status === "off") {
              console.log("CSRF token is invalid or expired");
              Cookies.remove('csrftoken');
              localStorage.removeItem('csrftoken');
              return false;
          }
          axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
          localStorage.setItem('csrftoken', csrfToken);
          return true;
      } catch (error) {
          console.error("Error checking CSRF token:", error);
          Cookies.remove('csrftoken');
          localStorage.removeItem('csrftoken');
          return false;
      }
  }
  return false;
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
      const response = await axios.get("/api/csrf-token");
      const csrfToken = response.data.csrf_token;
      console.log(csrfToken);
      axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
      localStorage.setItem('csrftoken', csrfToken);
      Cookies.set('csrftoken', csrfToken, { path: '/', secure: true, sameSite: 'Strict' });
  } catch (error) {
      console.error("Error fetching CSRF token:", error);
      throw error;
  }
}
