<template>
  <NavIndex></NavIndex>
  <div class="container">
    <div class="login-form">
      <div class="card">
        <h2 class="card-header text-center mb-4 oswald-header">Log in</h2>
        <form id="loginForm" @submit.prevent="loginUser">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              name="username"
              class="form-control"
              placeholder="Enter your username"
              required
              autofocus
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              name="password"
              class="form-control"
              placeholder="Enter your password"
              required
            />
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
import { setAccessToken } from "../../utils/Api/auth";
import api from "../../utils/Api/api";
import { validateForm } from "../../utils/Api/form";
import NavIndex from "./NavIndex.vue";

export default {
  name: "CompLogin",
  components: {
    'NavIndex': NavIndex
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    async loginUser() {
      try {
        validateForm(0, this.form);

        const response = await api.post("user/login/", {
          username: this.form.username,
          password: this.form.password,
        });
        if (response.data.access) 
          setAccessToken(response.data.access);
        else
          throw ("Error. No access token provided")

        this.$router.push("/home");
      } catch (error) {
        console.error('Registration error:', error.response);

        // Check if error.response exists
        if (error.response) {
          // Extract error messages
          const status = error.response.status;
          const message = error.response.data.message || 'An error occurred.';
          const errors = error.response.data.errors || {};

          // Format error message
          let errorMessage = `Login failed. ${message}`;
          if (Object.keys(errors).length > 0) {
            errorMessage += '\nErrors:\n';
            for (const [field, msgs] of Object.entries(errors)) {
              errorMessage += `${field}: ${msgs.join(', ')}\n`;
            }
          }

          // Show error message
          alert(errorMessage);
        } else {
          // Handle cases where error.response is not available
          alert('Registration failed. Please try again later.');
        }
      }
    },
  },
};
</script>
