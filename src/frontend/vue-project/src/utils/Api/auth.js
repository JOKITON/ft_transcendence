// utils/auth.js
import api from './api'

export function setAuthHeader() {
  const accessToken = localStorage.getItem('access_token');
  if (accessToken) {
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
  }
}

export function setAccessToken(accessToken) {
  localStorage.setItem('access_token', accessToken);
  setAuthHeader(); // Update headers with the new token
}

export function setRefreshToken(refreshToken) {
  localStorage.setItem('refresh_token', refreshToken);
}

export function removeAccessToken() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  api.defaults.headers.common['Authorization'] = "";
}

export async function refreshAuthToken() {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    const response = await api.post('/user/token/refresh/', {
      refresh: refreshToken,
    }
    );

    const newAccessToken = response.data.access;
    const newRefreshToken = response.data.refresh;
    if (newAccessToken) {
      setAccessToken(newAccessToken);
    }
    if (newRefreshToken)
      setRefreshToken(newRefreshToken);

    return true;
  } catch (error) {
    console.error(
      "Refresh token error:",
      error.response ? error.response.data : error.message
    );
    alert("Session expired. Please log in again.");
    return false;
  }
}

export async function checkAndRefreshToken() {
  try {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      setAuthHeader();
      const response = await api.post('/user/token/verify/', {
        token: accessToken,
      });

      if (response.status === 200) {
        return true; // Token is still valid
      }
    }
    else
      console.log('No token found. Redirecting to login.');
      return false;
  } catch (error) {
    const response = error.response;
    switch (response.data.code) {
      case 'expired':
        console.log('Token expired. Attempting to refresh.');
        return (await refreshAuthToken());

      case 'token_not_valid':
        console.log('Token invalid. Redirecting to login.');
        removeAccessToken();
        return false;

      case 'missing':
        console.log('Token missing. Redirecting to login.');
        removeAccessToken();
        return false;

      default:
        console.error('Unexpected token status:', response.data.status);
        removeAccessToken();
        return false;
    }
  }
}

export { api }