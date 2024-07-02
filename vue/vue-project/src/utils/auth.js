// utils/auth.js
import axios from "axios";

export default async function validateAuthToken() {
  const authToken = localStorage.getItem("auth-token");
  if (!authToken) return false;

  try {
    const response = await axios.get("/api/validate-token", {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
    return response.data.is_valid;
  } catch (error) {
    console.error(
      "Token validation error:",
      error.response ? error.response.data : error.message
    );
    return false;
  }
}
