// utils/auth.js
import { api } from "../main";
// import Cookies from 'js-cookie';

export async function refreshAuthToken() {
  try {
    const response = await api.post("/api/token/refresh/");
    console.log(response);
    return true;
  }
  catch (error) {
    console.error(
      "Login error:",
      error.response ? error.response.data : error.message
    );
    // Handle login error (e.g., show error message to user)
    alert(
      "Login failed. " +
        (error.response ? error.response.data.detail : error.message)
    );
    return false;
  }
}
