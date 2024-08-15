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
import type UserRequest from '@/Models/User/UserRequest'
import type UserResponse from '@/Models/User/UserResponse'
import { useRouter } from 'vue-router'
import { ref, inject } from 'vue'
import type Api from '@/utils/Api/Api'

const api = inject('$api') as Api<UserRequest, UserResponse>
const router = useRouter()

const form = ref<UserRequest>({
  username: '',
  password: ''
})

const handleSubmit: () => Promise<void> = async () => {
  try {
    console.log('this is my api global', api)
    const response: UserResponse = await api.post<UserResponse>('login', form.value)
    if (response.status !== 200) {
      window.alert('An error occurred while submitting the form')
    } else if (response.token === undefined) {
      window.alert('An error occurred while submitting the form')
    } else {
      //this.api.setAuthHeader(response.token.accessToken)
      //api.setAuthHeader(response.token.accessToken)
      localStorage.setItem('accessToken', response.token.accessToken)
      localStorage.setItem('refreshToken', response.token.refreshToken)
      api.setAuthHeader(response.token.accessToken)
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
