<template>
  <NavIndex></NavIndex>
  <div class="container">
    <div class="login-form">
      <div class="card">
        <h2 class="card-header text-center mb-4 oswald-header">Log in</h2>
        <form id="loginForm" @submit.prevent="handleSubmit">
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
            <label for="password" class="form-label">Password</label>
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
            <button type="submit" class="btn btn-primary btn-block">Log in</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import NavIndex from '../views/public/NavIndex.vue'
import Api from '../utils/Api/Api'
import { ref } from 'vue'
import type UserLoginResponse from '@/Models/User/Login/UserLoginResponse'
import type UserLoginRequest from '@/Models/User/Login/UserLoginRequst'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref<UserLoginRequest>({
  username: '',
  password: ''
})
const handleSubmit = async (): Promise<void> => {
  const apiInstance = new Api()
  try {
    const response = await apiInstance.post<UserLoginResponse>('login', form.value)
    console.log('Submitting form:', response)
    console.log('Form submitted successfully:', response)

    form.value = {
      username: '',
      password: ''
    }
    router.push('/')
  } catch (error: any) {
    console.error('An error occurred while submitting the form:', error)
    error.value = 'An error occurred while submitting the form'
  }
}
</script>
