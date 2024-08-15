<template>
  <NavIndex></NavIndex>
  <div class="container">
    <div class="login-form">
      <div class="card">
        <h2 class="card-header text-center mb-4 oswald-header">Register</h2>
        <form id="registerForm" @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              name="username"
              class="form-control"
              placeholder="Enter your username"
              required
              autofocus
            />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              name="email"
              class="form-control"
              placeholder="Enter your email"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">New Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              name="password"
              class="form-control"
              placeholder="Enter your password"
              required
            />
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-block">Register</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import NavIndex from '../views/public/NavIndex.vue'
import type UserRequest from '@/Models/User/UserRequst'
import type UserResponse from '@/Models/User/UserResponse'
import { useRouter } from 'vue-router'
import { ref, inject } from 'vue'
import type Api from '@/utils/Api/Api'

const api: Api<UserRequest, UserResponse> = inject('$api') as Api<UserRequest, UserResponse>
const router = useRouter()

const form = ref<UserRequest>({
  username: '',
  password: '',
  email: ''
})

const handleSubmit = async (): Promise<void> => {
  try {
    console.debug('Submitting form:', form.value)

    console.log('Form submitted successfully:', form.value)
    const response: UserResponse = await api.post<UserResponse>('register', form.value)
    if (response.status == 400) {
      console.error('error de registro')
    } else {
      console.log('Form submitted successfully:', response)
      router.push('/login')
    }
  } catch (error: any) {
    console.error('An error occurred while submitting the form:', error)
    error.value = 'An error occurred while submitting the form'
  }
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
