import Cookies from 'js-cookie';
import { api } from '../main'; // Import the api instance from main.js

// Function to get CSRF token from cookies using js-cookie
function getCsrfToken() {
    return Cookies.get('csrftoken');
}

// Function to check if CSRF cookie is valid
async function checkCSRF() {
    const csrfToken = getCsrfToken();
  
    if (csrfToken) {
        try {
            const response = await api.get("/api/csrf/");
            if (response.data.status === "off") {
                console.log("CSRF token is invalid or expired");
                Cookies.remove('csrftoken', { path: '/' });
                return false;
            }
            api.defaults.headers.common['X-CSRFToken'] = response.headers["x-csrftoken"];
            return true;
        } catch (error) {
            console.error("Error checking CSRF token:", error);
            Cookies.remove('csrftoken', { path: '/' });
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
        const response = await api.get("/api/csrf/");
        const csrfToken = response.headers["x-csrftoken"];

        // Set CSRF token in Axios defaults and cookies
        api.defaults.headers.common['X-CSRFToken'] = csrfToken;
    } catch (error) {
        console.error("Error fetching CSRF token:", error);
        throw error;
    }
}
