// utils/api.js
import Cookies from "js-cookie";
import axios from "axios";
import { setAuthHeaderFromCookie } from "./auth";

// Create an Axios instance
const api = axios.create({
  baseURL: '/api/',
  timeout: 30000,
  withCredentials: true, // Ensure cookies are sent with requests
  xsrfHeaderName: "X-CSRFToken",
  xsrfCookieName: "csrftoken",
});

// Interceptor to handle token refresh
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = Cookies.get("refresh_token");
        if (refreshToken) {
          const response = await api.post("token/refresh/", { refresh: refreshToken });
          const newAccessToken = response.data.access;
          Cookies.set("access_token", newAccessToken, { secure: true, sameSite: "Lax" });
          setAuthHeaderFromCookie();
          originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        }
      } catch (err) {
        if (err.response && err.response.status === 401) {
          // Refresh token is also invalid, log the user out
          console.error("Refresh token is invalid", err);
          Cookies.remove("access_token");
          Cookies.remove("refresh_token");
          window.location.href = "/login";  // Redirect to login page
        } else {
          console.error("Failed to refresh token", err);
        }
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

export default api;