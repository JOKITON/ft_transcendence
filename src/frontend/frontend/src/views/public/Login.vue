<template>
  <NavIndex></NavIndex>
  <div class="container">
    <div class="login-form m-5">
      <div class="data-card py-3 px-4">
        <h2 class="my-3 text-center data-card-title">Log in</h2>
        <form id="loginForm" @submit.prevent="handleSubmit">

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
              autofocus
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
            <button type="submit" class="btn data-button my-3">Log in</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

/* ----- IMPORTS ----- */

import { useRouter } from 'vue-router'
import { ref, inject } from 'vue'

import auth from '../../services/user/services/auth/auth.ts'

import NavIndex from './NavIndex.vue'

import type Api from '@/utils/Api/Api'
import type userRequest from '@/models/user/userRequest'
import type userResponse from '@/models/user/userResponse'


/* ----- VARIABLES ----- */

const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)
const router = useRouter()

const form: Ref<userRequest> = ref<userRequest>({
  username: '',
  password: ''
})


/* ----- HANDLE LOG IN ----- */

const handleSubmit: () => Promise<void> = async () => {
  try {
    const response: boolean = await Auth.login<userResponse>(form.value)
    if (response === true) {
      router.push('/home')
    }
    console.log('Login successful ', response)
  } catch (error: any) {
    window.alert('An error occurred while submitting the form')
    console.error('An error occurred while submitting the form:', error)
  }
}

</script>