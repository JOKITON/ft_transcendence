import Cookies from 'js-cookie';
import api from './api'; // Import the api instance from main.js

// Function to check if CSRF cookie is valid
async function checkCSRF() {
    try {
        const response = await api.get("csrf/check/");
        if (response.data.status === "off") {
            console.log("CSRF token is invalid or expired");
            Cookies.remove('csrftoken', { secure: true, httpOnly: true, sameSite: 'Lax', path: '/' });
            return false;
        }
        const csrfToken = response.data.csrftoken;
        api.defaults.headers.common['X-CSRFToken'] = csrfToken;
        Cookies.set('csrftoken', csrfToken, { secure: true, sameSite: 'Lax' });
        return true;
    } catch (error) {
        console.error("Error checking CSRF token:", error);
        Cookies.remove('csrftoken', { secure: true, httpOnly: true, sameSite: 'Lax', path: '/' });
    return false;
    }
}

// Function to fetch and set CSRF token
export default async function fetchAndSetCsrfToken() {
    try {
        const csrfTokenValid = await checkCSRF();
        if (csrfTokenValid) {
            console.log('Valid CSRF token found');
            return;
        }

        console.log('Fetching new CSRF token');
        // Fetch new CSRF token from the server
        const response = await api.get("csrf/");
        const csrfToken = response.headers["x-csrftoken"];

        // Set CSRF token in Axios defaults and cookies
        api.defaults.headers.common['X-CSRFToken'] = csrfToken;
        Cookies.set('csrftoken', csrfToken, { secure: true, sameSite: 'Lax' });
    } catch (error) {
        console.error("Error handling CSRF token:", error);
        // Handle error, maybe log out the user or prompt them to log in again
        throw error;
    }
}

export { fetchAndSetCsrfToken };