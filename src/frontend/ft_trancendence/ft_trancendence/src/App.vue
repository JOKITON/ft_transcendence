<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './views/HomeWorld.vue'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About</RouterLink>
      <RouterLink to="/contact">Contact</RouterLink>
    </nav>
  </header>
  <body>
    <RouterView />
  </body>
  <footer>
    <h1 align="center">este es el footer</h1>
  </footer>
</template>

<style scoped></style>
