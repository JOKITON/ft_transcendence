<template>
  <div class="container">
    <div class="login-form">
      <div class="card">
        <h2 class="card-header text-center mb-4 oswald-header">Register</h2>
        <form id="registerForm" @submit.prevent="registerUser">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input id="username" v-model="form.username" type="text" name="username" class="form-control"
              placeholder="Enter your username" required autofocus />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input id="email" v-model="form.email" type="email" name="email" class="form-control"
              placeholder="Enter your email" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">New Password</label>
            <input id="password" v-model="form.password" type="password" name="password" class="form-control"
              placeholder="Enter your password" required />
          </div>
          <div class="mb-3">
            <label for="password_confirm" class="form-label">Repeat Password</label>
            <input id="password_confirm" v-model="form.password_confirm" type="password" name="password_confirm"
              class="form-control" placeholder="Repeat your password" required />
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-block">
              Register
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
  name: "CompRegister",
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        password_confirm: "",
      },
    };
  },
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
    async registerUser() {
      try {
        this.validateForm();
        // Assuming you have the token in a global variable or fetched from an endpoint
        const csrfToken = await this.fetchCsrfToken();
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

        const response = await axios.post(
          "/api/register",
          {
            username: this.form.username,
            email: this.form.email,
            password: this.form.password,
            password_confirm: this.form.password_confirm,
          },
        );

        console.log("Registration successful:", response.data);
        // Handle successful registration (e.g., show success message, redirect)
      } catch (error) {
        console.error(
          "Registration error:",
          error.response ? error.response.data : error.message,
        );
        // Handle registration error (e.g., show error message to user)
        alert(
          "Registration failed. " +
          (error.response ? error.response.data.message : error.message),
        );
      }
    },
    validateForm() {
      if (this.form.password.length < 8) {
        throw new Error("Password must be at least 8 characters long");
      }

      if (!this.validateEmail(this.form.email)) {
        throw new Error("Invalid email format");
      }

      if (this.form.password !== this.form.password_confirm) {
        throw new Error("Passwords do not match.");
      }
    },
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
  },
};
</script>

<style scoped>
/* Your component-specific styles */
</style>
