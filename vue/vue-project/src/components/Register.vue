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
import { validateForm } from "../utils/csrf";

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
    async registerUser() {
      try {
        validateForm(1, this.form);

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
        this.$router.push('/login');
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
  },
};
</script>

<style scoped>
/* Your component-specific styles */
</style>
