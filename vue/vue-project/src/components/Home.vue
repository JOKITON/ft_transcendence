<template>
  <div>
    <div class="alert alert-success" role="alert">
      <h4 class="alert-heading">Welcome to Pong!</h4>
      <p>
        Congrats! You logged on! This is the Homepage.
      </p>
      Do not hesitate to
      <form id="logoutUser" @submit.prevent="logoutUser">
        <button type="submit" class="btn btn-primary btn-block"> log out</button>
      </form>
      <hr />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { fetchCsrfToken } from "../utils/csrf";

export default {
  name: "loginHome",
  data() {
    return {
    };
  },
  methods: {
    async logoutUser() {
      try {
        const csrfToken = await fetchCsrfToken();
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

        const response = await axios.post(
          "/api/logout",
          {
          },
        );

        console.log("Logout successful:", response.data);
        localStorage.removeItem('user');
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
  },
};
</script>

<style scoped>
/* Your component-specific styles */
</style>