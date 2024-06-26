<template>
	<div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a
        class="navbar-brand"
        href="home"
        data-link="home"
      >SPA Example</a>
      <div
        id="navbarNav"
        class="collapse navbar-collapse"
      >
        <ul class="navbar-nav">
          <li class="nav-item">
            <a
              class="nav-link"
              href="home"
              data-link="home"
            >Home</a>
          </li>
          <li class="nav-item">
            <a
              class="nav-link"
              href="login"
              data-link="login"
            >Login</a>
          </li>
          <li class="nav-item">
            <a
              class="nav-link"
              href="register"
              data-link="register"
            >Register</a>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'pageIndex',
}
</script>

<style scoped>
</style>
