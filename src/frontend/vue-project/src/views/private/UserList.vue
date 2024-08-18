<template>
	<NavHome></NavHome>
	<main class="px-3">
		<div>
			<ul>
				<li v-for="user in users" :key="user.id">
					<strong>{{ user.username }}</strong> - {{ user.email }}
				</li>
			</ul>
		</div>
	</main>
</template>

<script>
import api from "../../utils/Api/api";
import User from "../../utils/User/UserModel";
import NavHome from "./NavHome.vue";

export default {
	name: 'userList',
	components: {
		NavHome: NavHome
	},
	data() {
		return {
			users: [],
			username: '',
		}
	},
	async created() {
		// Fetch or set the username when the component is created
		await this.fetchUserList()
		await this.fetchUsername()
	},
	methods: {
		async fetchUserList() {
			try {
				const response = await api.get("admin/users/");
				const data = response.data;
				this.users = data.map(user => new User(user.id, user.username, user.email));
			} catch (error) {
				console.error(
					'Error fetching users:',
					error.response ? error.response.data : error.message
				)
				alert(error.response.data.detail)
				this.$router.push('/home');
			}
		},
		async fetchUsername() {
			try {
				const response = await api.get("user/whoami/");
				this.username = response.data.username; // Replace with your actual response structure
			} catch (error) {
				console.error(
					'Error fetching username:',
					error.response ? error.response.data : error.message
				)
			}
		},
	}
}
</script>

<style>

</style>