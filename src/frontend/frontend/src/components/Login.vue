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
import type UserRequest from '@/Models/User/UserRequest'
import type UserResponse from '@/Models/User/UserResponse'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const apiInstance: Api<UserRequest, UserResponse> = new Api<UserRequest, UserResponse>()
const router = useRouter()

const form = ref<UserRequest>({
  username: '',
  password: ''
})

const handleSubmit: () => Promise<void> = async () => {
  try {
    const response: UserResponse = await apiInstance.post<UserResponse>('login', form.value)
    if (response.status !== 200) {
      window.alert('An error occurred while submitting the form')
      throw new Error('An error occurred while submitting the form')
    } else if (response.token === undefined) {
      throw new Error('An error occurred while submitting the form')
    } else {
      localStorage.setItem('accessToken', response.token.accessToken)
      localStorage.setItem('refreshToken', response.token.refreshToken)
      console.log('Login successful')
      router.push('/pong')
    }
  } catch (error: any) {
    //pop up error Message
    window.alert('An error occurred while submitting the form')

    console.error('An error occurred while submitting the form:', error)
    error.value = 'An error occurred while submitting the form'
  }
}
</script>
