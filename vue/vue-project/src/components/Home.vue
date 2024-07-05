<template>
  <div class="home-container">
    <nav class="navbar">
      <h1>Welcome to Pong!</h1>
      <ul class="nav-links">
        <li><router-link to="/game">Game</router-link></li>
        <li><router-link to="/friend-list">Friend List</router-link></li>
        <li><router-link to="/profile">Profile</router-link></li>
      </ul>
      <button @click="logoutUser" class="logout-button">Log out</button>
    </nav>
    <main>
      <section class="welcome-section">
        <div class="alert alert-success" role="alert">
          <h3 class="alert-heading">Hello, {{ username }}!</h3>
          <p>Congrats! You logged in successfully. This is the Homepage.</p>
          <p>Do not hesitate to explore and enjoy your time here.</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { api } from "../main";

export default {
  name: "loginHome",
  methods: {
    async logoutUser() {
      try {
        const response = await api.post("/api/logout/");

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

<style>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  background-color: #333;
  color: #fff;
  padding: 1rem;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 1rem;
}

.nav-links li {
  margin: 0;
}

.nav-links a {
  color: #fff;
  text-decoration: none;
}

.nav-links a:hover {
  text-decoration: underline;
}

.logout-button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #d32f2f;
}

.welcome-section {
  margin: 2rem 2rem;
}

.alert {
  padding: 1rem;
  border-radius: 5px;
  background-color: #d4edda;
  color: #155724;
}

.alert-heading {
  margin-top: 0;
}
</style>