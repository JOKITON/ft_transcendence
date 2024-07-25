<setup setup lang="ts">
export default {
  name: pong
}
</setup>

<script setup lang="ts">
import Three from '@/service/pong/Three'
const three = Three()

three.resize(window.innerWidth - 500, window.innerHeight - 300)
</script>

<template>
  <h1 align="center">Pong</h1>
</template>

<style scoped>
h1 {
  color: blue;
  align-items: center;
  justify-content: center;
}
</style>
