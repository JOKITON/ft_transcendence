<template>
  <div class="container">
    <div class="login-form">
      <div class="card">
        <h2 class="card-header text-center mb-4 oswald-header">Log in</h2>
        <form id="loginForm" @submit.prevent="loginUser">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input id="username" v-model="form.username" type="text" name="username" class="form-control"
              placeholder="Enter your username" required autofocus />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input id="password" v-model="form.password" type="password" name="password" class="form-control"
              placeholder="Enter your password" required />
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-block">
              Log in
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
//import fetchCsrfToken from "../utils/csrf";

export default {
  name: "CompLogin",
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  // Example API call in Register.vue component
  methods: {
    async fetchCsrfToken() {
      try {
        const response = await axios.get('/api/csrf-token');
        return response.data.csrfToken;
      } catch (error) {
        console.error('Error fetching CSRF token:', error);
        throw error;
      }
    },
    async loginUser() {
      try {
        this.validateForm();
        // Assuming you have the token in a global variable or fetched from an endpoint
        const csrfToken = await this.fetchCsrfToken();
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

        const response = await axios.post("/api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.form.username,
            password: this.form.password,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message); // Throw error with server message
        }

        console.log("Login successful:", data);
        // Handle successful registration (e.g., show success message, redirect)
      } catch (error) {
        console.error("Login error:", error.message);
        // Handle registration error (e.g., show error message to user)
        alert("Login failed. " + error.message);
      }
    },
    validateForm() {
      if (this.form.password.length < 8) {
        throw new Error("Password must be at least 8 characters long");
      }
    },
  },
};
</script>
