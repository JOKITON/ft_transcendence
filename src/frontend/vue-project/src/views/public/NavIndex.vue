<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <!-- deberia poner un logo guay usemos el del favicon por ahora -->
    <img
      src="../../assets/images/logo.png"
      width="30"
      height="30"
      class="d-inline-block align-top"
      alt=""
    />
    <div id="navbarNav" class="collapse navbar-collapse" align="center">
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
  name: 'NavIndex'
}
</script>

<style></style>
