<template>
	<div class="container">
		<div class="login-form">
			<div class="card">
				<h2 class="card-header text-center mb-4 oswald-header">Register</h2>
				<form @submit.prevent="registerUser" id="registerForm">
					<div class="mb-3">
						<label for="username" class="form-label">Username</label>
						<input v-model="form.username" type="text" id="username" name="username" class="form-control"
							placeholder="Enter your username" required autofocus>
					</div>
					<div class="mb-3">
						<label for="email" class="form-label">Email</label>
						<input v-model="form.email" type="email" id="email" name="email" class="form-control"
							placeholder="Enter your email" required>
					</div>
					<div class="mb-3">
						<label for="password" class="form-label">New Password</label>
						<input v-model="form.password" type="password" id="password" name="password"
							class="form-control" placeholder="Enter your password" required>
					</div>
					<div class="mb-3">
						<label for="password_confirm" class="form-label">Repeat Password</label>
						<input v-model="form.password_confirm" type="password" id="password_confirm"
							name="password_confirm" class="form-control" placeholder="Repeat your password" required>
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
	data() {
		return {
			form: {
				username: '',
				email: '',
				password: '',
				password_confirm: ''
			}
		};
	},
	// Example API call in Register.vue component
	methods: {
		async registerUser() {
			try {
				const response = await fetch('http://app:8000/api/register', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						// Include CSRF token if required by backend
						// 'X-CSRFToken': this.getCsrfToken()
					},
					body: JSON.stringify({
						username: this.form.username,
						email: this.form.email,
						password: this.form.password,
						// Add additional fields as needed
					})
				});

				if (!response.ok) {
					throw new Error('Registration failed');
				}

				const data = await response.json();
				console.log('Registration successful:', data);

				// Redirect or handle success accordingly
			} catch (error) {
				console.error('Registration error:', error);
				// Handle registration error (e.g., show error message to user)
				alert('Registration failed. Please try again.');
			}
		},
	},
};
</script>

<style scoped>
/* Your component-specific styles */
</style>
