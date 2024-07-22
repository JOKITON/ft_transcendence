import Cookies from 'js-cookie';
import api from './api'; // Import the api instance from main.js

// Function to check if CSRF cookie is valid
async function checkCSRF() {
    try {
        const response = await api.get("csrf/check/");
        if (response.data.status === "off") {
            console.log("CSRF token is invalid or expired");
            Cookies.remove('csrftoken', { path: '/' });
            return false;
        }
        const csrfToken = response.data.csrftoken;
        console.log(csrfToken);
        api.defaults.headers.common['X-CSRFToken'] = csrfToken;
        Cookies.set('csrftoken', csrfToken, { secure: true, sameSite: 'Lax' });
        return true;
    } catch (error) {
        console.error("Error checking CSRF token:", error);
        Cookies.remove('csrftoken', { path: '/' });
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
        const response = await api.get("csrf/");
        const csrfToken = response.headers["x-csrftoken"];

        console.log(csrfToken);
        // Set CSRF token in Axios defaults and cookies
        api.defaults.headers.common['X-CSRFToken'] = csrfToken;
        Cookies.set('csrftoken', csrfToken, { secure: true, sameSite: 'Lax' });
    } catch (error) {
        console.error("Error fetching CSRF token:", error);
        throw error;
    }
}
