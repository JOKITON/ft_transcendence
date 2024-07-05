<template>
  <div class="home-container">
    <nav class="navbar">
      <h1>Welcome to Pong!</h1>
      <button @click="logoutUser" class="logout-button">Log out</button>
    </nav>
    
    <main>
      <section class="welcome-section">
        <div class="alert alert-success" role="alert">
          <h4 class="alert-heading">Hello, {{ username }}!</h4>
          <p>
            Congrats! You logged in successfully. This is the Homepage.
          </p>
          <p>
            Do not hesitate to explore and enjoy your time here.
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "loginHome",
  methods: {
    async logoutUser() {
      try {
        const response = await axios.post("/api/logout/");

        // Update the CSRF token
        axios.defaults.headers.common['X-CSRFToken'] = response.data.csrf_token;

        // Remove auth token from localStorage
        localStorage.removeItem('auth-token');

        console.log("Logout successful:", response.data);

        // Redirect to login page
        this.$router.push('/login');
      } catch (error) {
        console.error(
          "Logout error:",
          error.response ? error.response.data : error.message,
        );
        // Handle logout error (e.g., show error message to user)
        alert(
          "Logout failed. " +
          (error.response ? error.response.data.message : error.message),
        );
      }
    }
  }
};
</script>

<style scoped>
/* Your component-specific styles */
</style>