<template>
	<div class="container">
		<div class="login-form">
			<div class="card">
				<h2 class="card-header text-center mb-4 oswald-header">Register</h2>
				<form id="registerForm" method="POST" action="{% url 'register' %}">
					{% csrf_token %}
					<div class="mb-3">
						<label for="username" class="form-label">Username</label>
						<input type="text" id="username" name="username" class="form-control" placeholder="Enter your username" required autofocus>
					</div>
					<div class="mb-3">
						<label for="email" class="form-label">Email</label>
						<input type="email" id="email" name="email" class="form-control" placeholder="Enter your email" required>
					</div>
					<div class="mb-3">
						<label for="password" class="form-label">New Password</label>
						<input type="password" id="password" name="password" class="form-control" placeholder="Enter your password" required>
					</div>
					<div class="mb-3">
						<label for="password_confirm" class="form-label">Repeat Password</label>
						<input type="password" id="password_confirm" name="password_confirm" class="form-control" placeholder="Enter your password" required>
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

export default {
  name: 'compRegister',
}
</script>
