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
import NavIndex from './NavIndex.vue'
import type userRequest from '@/models/user/userRequest'
import type userResponse from '@/models/user/userResponse'
import { useRouter } from 'vue-router'
import { ref, inject } from 'vue'
import type Api from '@/utils/Api/Api'
import auth from '../../services/user/services/auth/auth.ts'

const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)
const router = useRouter()

const form: Ref<userRequest> = ref<userRequset>({
  username: '',
  password: ''
})

const handleSubmit: () => Promise<void> = async () => {
  try {
    const response: boolean = await Auth.login<userResponse>(form.value)
    if (response === true) {
      router.push('/pong')
    }
    console.log('Login successful ', response)
  } catch (error: any) {
    window.alert('An error occurred while submitting the form')
    console.error('An error occurred while submitting the form:', error)
  }
}
</script>
