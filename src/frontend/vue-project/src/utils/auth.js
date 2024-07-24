// utils/auth.js
import Cookies from 'js-cookie'
import api from './api'

export function setAuthHeader(accessToken, refreshToken) {
  if (accessToken && refreshToken) {
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
    Cookies.set('refresh_token', refreshToken, { secure: true, httpOnly: true, sameSite: 'Lax' })
    Cookies.set('access_token', accessToken, { secure: true, httpOnly: true, sameSite: 'Lax' })
    setTokens(accessToken, refreshToken)
  }
}

// Function to set Authorization header
export function setAuthHeaderFromCookie() {
  const accessToken = Cookies.get('access_token')
  if (accessToken) {
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
  } else {
    delete api.defaults.headers.common['Authorization']
  }
}

export function removeLocalData() {
    // Clear tokens from localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('token_expiry');

    // Clear tokens from cookies (if used)
    Cookies.remove('access_token', { path: '/' });
    Cookies.remove('refresh_token', { path: '/' });
}

function setTokens(accessToken, refreshToken) {
  const expiry = new Date().getTime() + (5 * 60 * 1000); // 5 minutes from now
  localStorage.setItem('access_token', accessToken);
  localStorage.setItem('refresh_token', refreshToken);
  localStorage.setItem('token_expiry', expiry);
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
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('token_expiry');
    return false;
  }
}

const GRACE_PERIOD = 5 * 60 * 1000; // 5 minutes grace period

export async function checkAndRefreshToken() {
  const expiry = localStorage.getItem('token_expiry');
  const now = new Date().getTime();


  if (!expiry) return false;
  // Check if the token is about to expire within the grace period
  if (now >= (parseInt(expiry) - GRACE_PERIOD)) {
    // Token has expired, attempt to refresh it
    const refreshed = await refreshAuthToken();
    return refreshed;
  }

  return true; // Token is still valid
}

export { api }
