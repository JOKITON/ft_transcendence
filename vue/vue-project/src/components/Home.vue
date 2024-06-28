<template>
  <div>
    <div class="alert alert-success" role="alert">
      <h4 class="alert-heading">Welcome to Pong!</h4>
      <p>
        You need to either 
        <router-link class="" to="/login" data-link="login">log in</router-link> 
        or 
        <router-link class="" to="/register" data-link="register">sign up</router-link>.
      </p>
      <hr>
      <p class="mb-0">Things seem pretty boring here... Do you think you can beat me in a Pong game?</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'compHome',
}
</script>