<template>
  <header class="p-3 nav-background">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"></div>
      <ul class="nav col-lg-auto me-lg-auto mb-md-0 nav-flex">
        <li>
          <img
            src="../../assets/images/logo.png"
            width="30"
            height="30"
            class="d-inline-block align-top"
            alt=""
          />
        </li>
        <li><a @click="goToHome" class="nav-link px-4 nav-item">Home</a></li>
        <li><a @click="goToLogin" class="nav-link px-4 nav-item">Login</a></li>
        <li><a @click="goToRegister" class="nav-link px-4 nav-item">Register</a></li>
      </ul>
    </div>
  </header>
</template>

<script setup lang="ts">

import { useRouter } from 'vue-router'

const router = useRouter()


/* ----- REDIRECCIONES A VISTAS ----- */

const goToHome = () => {
  router.push('/')
}

const goToLogin= () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}
</script>
