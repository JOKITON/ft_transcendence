<template>
	<nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link class="nav-link" to="/">SPA Example</router-link>
      <div id="navbarNav" class="collapse navbar-collapse">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
        </ul>
      </div>
    </nav>
</template>

<script>
export default {
  name: "NavIndex",
};
</script>

<style>

</style>
