// utils/csrf.js
import axios from 'axios';

// Fetch CSRF token from Django and set it in Axios
export default async function fetchAndSetCsrfToken() {
    try {
        const response = await axios.get('/api/csrf-token'); // Make an initial request to get CSRF token
        const csrfToken = response.data.csrfToken;

        // Set Axios default headers
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

        // Optionally, you can store it in localStorage or cookies
        // localStorage.setItem('csrfToken', csrfToken);

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
