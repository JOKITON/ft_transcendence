// utils/csrf.js
import axios from 'axios';

export async function fetchCsrfToken() {
  try {
    const response = await axios.get('/api/csrf-token');
    return response.data.csrfToken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    throw error;
  }
}

export function validateForm(reg, form) {
  if (form.password.length < 8) {
    throw new Error("Password must be at least 8 characters long");
  }

  if (reg == 1 && !validateEmail(form.email)) {
    throw new Error("Invalid email format");
  }

  if (reg == 1 && form.password !== form.password_confirm) {
    throw new Error("Passwords do not match.");
  }
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}
