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
				this.validateForm();
				const response = await fetch('/api/register', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						username: this.form.username,
						email: this.form.email,
						password: this.form.password,
						password_confirm: this.form.password_confirm  // Add the confirmation password here
					})
				});

				const data = await response.json();

				if (!response.ok) {
					throw new Error(data.message);  // Throw error with server message
				}

				console.log('Registration successful:', data);
				// Handle successful registration (e.g., show success message, redirect)

			} catch (error) {
				console.error('Registration error:', error.message);
				// Handle registration error (e.g., show error message to user)
				alert('Registration failed. ' + error.message);
			}
		},
		validateForm() {
			if (this.form.password.length < 8) {
				throw new Error("Password must be at least 8 characters long");
			}

			if (!this.validateEmail(this.form.email)) {
				throw new Error("Invalid email format");
			}

			if (this.form.password !== this.form.password_confirm) {
				throw new Error("Passwords do not match.");
			}
		},

		validateEmail(email) {
			const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
			return re.test(email);
		}
	},
};
</script>

<style scoped>
/* Your component-specific styles */
</style>
