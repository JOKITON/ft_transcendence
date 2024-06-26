<template>
  <div class="container">
		<nav class="navbar navbar-expand-lg navbar-light bg-light">
			<a class="navbar-brand" href="home" data-link="home">SPA Example</a>
			<div class="collapse navbar-collapse" id="navbarNav">
				<ul class="navbar-nav">
					<li class="nav-item">
						<a class="nav-link" href="home" data-link="home">Home</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="login" data-link="login">Login</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="register" data-link="register">Register</a>
					</li>
				</ul>
			</div>
		</nav>
	<Home/>
	<Login/>
	<Register/>
	</div>
</template>

<script>
import Home from './components/Home.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';

export default {
  name: 'App',
  components: {
    Home, Login, Register,
  }
}
</script>
