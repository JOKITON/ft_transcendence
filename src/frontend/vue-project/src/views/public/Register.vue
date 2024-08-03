<template>
  <NavIndex></NavIndex>
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
            <button type="submit" class="btn btn-primary btn-block">Register</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavIndex from './NavIndex.vue'
import { validateForm } from '../../utils/Api/form'
import api from '../../utils/Api/api'

export default {
  name: 'CompRegister',
  components: {
    NavIndex: NavIndex
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        password_confirm: ''
      }
    }
  },
  methods: {
    async registerUser() {
      try {
        // Validate form data before sending request
        validateForm(1, this.form);

        // Make the API request
        const response = await api.post("user/register/", {
          username: this.form.username,
          email: this.form.email,
          password: this.form.password,
        });

        // Handle successful registration
        this.$router.push('/login');
        // Optionally show a success message
        alert('Registration successful. Please log in.');

      } catch (error) {
        console.error('Registration error:', error.response);

        // Check if error.response exists
        if (error.response) {
          // Extract error messages
          const message = error.response.data.message || 'An error occurred.';
          const errors = error.response.data.errors || {};

          // Format error message
          let errorMessage = `Registration failed. ${message}`;
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
    }
  }
}
</script>

<style scoped>
/* Your component-specific styles */
</style>
