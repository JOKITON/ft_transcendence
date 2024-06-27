<template>
<div class="container">
	<nav class="navbar navbar-expand-lg navbar-light bg-light">
	<a class="navbar-brand" href="/" data-link="home">SPA Example</a>
	<div class="collapse navbar-collapse" id="navbarNav">
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
	<router-view></router-view>
</div>
</template>

<script>
export default {
name: 'App',
}
</script>