<template>
  <NavIndex></NavIndex>
  <div class="container">
    <div class="login-form m-5">
      <div class="data-card py-3 px-4">
        <h2 class="my-3 text-center data-card-title">Register</h2>
        <form id="registerForm" @submit.prevent="handleSubmit">
          <!-- Enter Username -->
          <div class="mb-3">
            <label for="username" class="data-label">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              name="username"
              class="data-control data-placeholder"
              placeholder="Enter your username"
              required
            />
          </div>

          <!-- Enter Nickname -->
          <div class="mb-3">
            <label for="nickname" class="data-label">Nickname</label>
            <input
              id="nickname"
              v-model="form.nickname"
              type="text"
              name="nickname"
              class="data-control data-placeholder"
              placeholder="Enter your nickname"
              required
            />
          </div>

          <!-- Enter Email -->
          <div class="mb-3">
            <label for="email" class="data-label">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              name="email"
              class="data-control data-placeholder"
              placeholder="Enter your email"
              required
            />
          </div>

          <!-- Enter Password -->
          <div class="mb-3">
            <label for="password" class="data-label">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              name="password"
              class="data-control data-placeholder"
              placeholder="Enter your password"
              required
            />
          </div>

          <!-- Submit Button -->
          <div class="d-grid gap-2">
            <button type="submit" class="btn data-button my-3">Register</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/* ----- IMPORTS ----- */

import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'

import type Api from '@/utils/Api/Api'

import auth from '@/services/auth/auth'

import NavIndex from './NavIndex.vue'

import type { userRequest } from '../../models/user/userRequest'
// import type { userResponse } from '../../models/user/userResponse'

/* ----- VARIABLES ----- */

const api: Api = inject('$api') as Api
const Auth = new auth(api)
const router = useRouter()

const form = ref<userRequest>({
  username: '',
  password: '',
  email: '',
  nickname: '',
  p_image: ''
})

/* ----- HANDLE REGISTER ----- */

const handleSubmit = async (): Promise<void> => {
  try {
    const response: boolean = await Auth.register(form.value)
    if (response === true) {
      router.push('/login')
    }
  } catch (error: any) {
    console.error('An error occurred while submitting the form:', error)
    error.value = 'An error occurred while submitting the form'
  }
}
</script>
