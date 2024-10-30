<template>
	<NavHome></NavHome>
	<div class="container">
		<div class="main-body">
			<div class="row gutters-sm">
				<div class="col-sm-6 mb-3">
					<div class="card h-100">
						<div class="card-body">
							<h6 class="d-flex align-items-center mb-3">Users List</h6>
							<ul class="list-group">
								<li v-for="user in users" :key="user.id"
									class="list-group-item d-flex justify-content-between align-items-center">
									<span>
										<span class="status-indicator bg-success">{{ user.username }}</span>
										<span class="badge bg-success">{{ user.status }}</span>
									</span>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import NavHome from './NavHome.vue'
import { ref, onMounted, inject } from 'vue'
import type Api from '@/utils/Api/Api'
import auth from '../../services/user/services/auth/auth.ts'
import { useRouter } from 'vue-router'

const router = useRouter()
const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)

const users = ref<User[]>([]);

interface User {
	id: number
	username: string
	nickname: string
	email: string,
}

onMounted(async () => {
	await fetchUserList()
})

const fetchUserList = async () => {
	try {
		const response = await api.get('friendship/users');
		const data = Object.values(response.data);
		users.value = data.filter(user => typeof user === 'object' && user.id && user.username);
	} catch (error: any) {
		console.error('Error fetching users:', error.response ? error.response.data : error.message);
		router.push('/home');
	}
}

</script>

<style scoped>
.main-body {
	padding: 15px;
}

.card {
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	border-radius: 0.25rem;
	background-color: #fff;
}

.h-100 {
	height: 100%;
}

.d-flex {
	display: flex;
}

.justify-content-between {
	justify-content: space-between;
}

.mb-3 {
	margin-bottom: 1rem;
}

.gutters-sm {
	margin-right: -8px;
	margin-left: -8px;
}

.gutters-sm > .col {
	padding-right: 8px;
	padding-left: 8px;
}

.status-indicator {
	width: 10px;
	height: 10px;
	margin-right: 10px;
	border-radius: 50%;
}

.bg-success {
	background-color: green;
}
</style>
