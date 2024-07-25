// utils/auth.js
import Cookies from 'js-cookie'
import api from './api'

export function setAuthHeader(accessToken) {
  if (accessToken) {
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
  }
}

// Example function to make an authenticated request
export async function refreshAuthToken() {
  try {
    const response = await api.post(
      '/user/token/refresh/', 
      {}, // No need to include the refresh token here if it's in cookies
      { withCredentials: true } // Ensure cookies are sent with the request
    );

    const newAccessToken = response.data.access;

    // Update auth headers if necessary
    setAuthHeader(newAccessToken);

    return true;
  } catch (error) {
    console.error(
      "Refresh token error:",
      error.response ? error.response.data : error.message
    );
    // Handle error
    alert("Session expired. Please log in again.");
    return false;
  }
}

export async function checkAndRefreshToken() {
  try {
    // Make a request to the server to verify the token
    const response = await api.get('/user/token/verify/', { withCredentials: true });

    console.log('Token verification response:', response.data);  // Log the response data

    if (response.data.status === 'valid') {
      return true; // Token is still valid
    }
  } catch (error) {
    const response = error.response;
    switch (response.data.status) {
      case 'expired':
        // Handle expired token
        console.log('Token expired. Attempting to refresh.');
        const refreshed = await refreshAuthToken();
        return refreshed;

      case 'invalid':
        // Handle invalid token
        console.log('Token invalid. Redirecting to login.');
        return false;

      case 'missing':
        // Handle missing token
        console.log('Token missing. Redirecting to login.');
        return false;

      default:
        console.error('Unexpected token status:', response.data.status);
        return false;
    }
  }
}

export { api }
