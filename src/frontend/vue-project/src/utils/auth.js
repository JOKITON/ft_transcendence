// utils/auth.js
import Cookies from "js-cookie";
import api from "./api";

export function setAuthHeader(accessToken, refreshToken) {
  if (accessToken && refreshToken) {
    api.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;
    Cookies.set('refresh_token', refreshToken, { secure: true, sameSite: 'Lax' });
    Cookies.set('access_token', accessToken, { secure: true, sameSite: 'Lax' });
  }
}

// Function to set Authorization header
export function setAuthHeaderFromCookie() {
  const accessToken = Cookies.get("access_token");
  if (accessToken) {
    api.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
}

// Function to refresh auth token
export async function refreshAuthToken() {
  try {
    let refreshToken = Cookies.get('refresh_token');
    const refreshToken2 = api.defaults.headers.common["Authorization"];
    if (!refreshToken) {
        refreshToken = refreshToken2;
        console.log(refreshToken);
    }
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await api.post('auth/token/refresh/', { refresh: refreshToken });
    const newAccessToken = response.data.access;
    const newRefreshToken = response.data.refresh;

    // Update the Authorization header with the new token
    setAuthHeader(newAccessToken, newRefreshToken);

    return true;
  } catch (error) {
    console.error(
      "Refresh token error:",
      error.response ? error.response.data : error.message
    );
    // Handle refresh token error (e.g., log out the user)
    alert(
      "Session expired. Please log in again. " +
        (error.response ? error.response.data.detail : error.message)
    );
    return false;
  }
}

export { api };
