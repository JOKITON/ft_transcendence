// utils/auth.js
import Cookies from 'js-cookie'
import api from './api'

export function setAuthHeader(accessToken, refreshToken) {
  if (accessToken && refreshToken) {
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
    Cookies.set('refresh_token', refreshToken, { secure: true, httpOnly: true, sameSite: 'Lax' })
    Cookies.set('access_token', accessToken, { secure: true, httpOnly:true, sameSite: 'Lax' })
  }
}

export function removeLocalData() {
    // Clear tokens from cookies
    Cookies.remove('access_token', { secure: true, httpOnly:true, sameSite: 'Lax' });
    Cookies.remove('refresh_token', { secure: true, httpOnly:true, sameSite: 'Lax' });
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
    const newRefreshToken = response.data.refresh || Cookies.get('refresh_token');

    // Update auth headers if necessary
    setAuthHeader(newAccessToken, newRefreshToken);

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
        await removeLocalData(); // Custom function to handle invalid token scenario
        return false;

      case 'missing':
        // Handle missing token
        console.log('Token missing. Redirecting to login.');
        await removeLocalData(); // Custom function to handle missing token scenario
        return false;

      default:
        console.error('Unexpected token status:', response.data.status);
        return false;
    }
  }
}

export { api }
