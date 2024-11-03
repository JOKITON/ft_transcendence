<template>
  <NavIndex></NavIndex>
  <div>
    <div class="block alert alert-success" role="alert">
      <h4 class="alert-heading">Welcome to Pong!</h4>
      <p>
        You need to either
        <router-link class="" to="/login" data-link="login">log in</router-link>
        or
        <router-link class="" to="/register" data-link="register">sign up</router-link>.
      </p>
      <hr />
      <p class="mb-0">
        Things seem pretty boring here... Do you think you can beat me in a Pong game?
      </p>
    </div>
  </div>
  <button
    :class="['pong-review', { active: showPongReview }]"
    @click="showPongReview = !showPongReview"
  >
    {{ showPongReview ? 'Hide Pong Game' : 'Show Pong Game' }}
  </button>
  <div class="pong-game-container" v-if="showPongReview">
    <PongReviewAI class="pong-game" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NavIndex from './NavIndex.vue'
import PongReviewAI from './PongReviewAI.vue'

let showPongReview = ref(false)
</script>

<style>
.pong-review {
  display: block;
  margin: 20px auto;
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pong-game {
  display: block;
  align-items: center;
  margin: 20px auto;
}

.pong-review:hover {
  background-color: #0056b3;
}

.block {
  padding: auto;
  margin: auto;
  width: 40%;
  text-align: center;
}
</style>
