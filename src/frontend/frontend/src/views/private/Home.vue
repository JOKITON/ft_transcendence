<template>
  <div class="pruebas">
    <NavHome></NavHome>
  </div>
  <main>
    <!-- Sección de bienvenida con el tema de Pong -->
    <section class="welcome-section">
      <div class="overlay"></div>
      <div class="welcome-content">
        <h1 class="h1-welcome">Welcome to Magic Super Mega Pong, {{ username }}</h1>
        <h2 class="h2-welcome">Challenge yourself and compete with players from around the world.</h2>
        <button @click="goToPong" class="btn btn-lg btn-primary">Start Playing</button>
      </div>
    </section>

    <!-- Sección de información personalizada -->
    <section class="info-section row">
      <div class="info-card d-flex flex-column justify-content-center col-md-4 col-sm-2">
        <h2 class="pt-2">Play a Game</h2>
        <p class="m-3 pt-4">Jump into a match and test your skills.</p>
        <button @click="goToPong" class="btn txoinas-button mt-3 mx-2">Play Now</button>
      </div>
      <div class="info-card  d-flex flex-column justify-content-center col-md-4">
        <h2 class="pt-2">Challenge Friends</h2>
        <p class="m-3 pt-4">Invite your friends and see who comes out on top.</p>
        <button @click="goToFriends" class="btn txoinas-button mt-3 mx-2">Challenge Friends</button>
      </div>
      <div class="info-card  d-flex flex-column justify-content-center col-md-4">
        <h2 class="pt-2">Profile Settings</h2>
        <p class="m-3 pt-4">Customize your avatar and update your profile information.</p>
        <button @click="goToSettings" class="btn txoinas-button mt-3 mx-2">Edit Profile</button>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import NavHome from './NavHome.vue'
import auth from '../../services/user/services/auth/auth.ts'
import type Api from '@/utils/Api/Api'

// Variables reactivas
const isProfileVisible = ref(false)
const isDropdownVisible = ref(false)
const username = ref('PongPlayer') // Valor inicial personalizado
const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)
const router = useRouter()

// Función para cerrar sesión
const logoutUser = async () => {
  try {
    const response = await Auth.logout()
    if (response.status === 200) {
      console.log('Logout successful:', response.data)
      Auth.removeAccessToken()
      router.push('/login')
    } else {
      console.error('Logout failed:', response.data)
      alert('Logout failed. ' + response.data.message)
      Auth.removeAccessToken()
    }
  } catch (error) {
    console.error('Logout error:', error.response ? error.response.data : error.message)
    alert('Logout failed. ' + (error.response ? error.response.data.message : error.message))
  }
}

// Función para obtener el nombre de usuario
const fetchUsername = async () => {
  try {
    const response = await Auth.whoami()
    username.value = response.username
  } catch (error) {
    console.error('Error fetching username:', error.response ? error.response.data : error.message)
  }
}

// Funciones de navegación
const goToHome = () => { 
  router.push('/home')
}

const goToPong = () => {
  router.push('/pong')
}

const goToSettings = () => {
  router.push('/edit-profile')
}

const goToProfile = () => {
  router.push('/profile')
}

const goToFriends = () => {
  router.push('/friends')
}

// Lifecycle hook similar a `created` en Options API
onMounted(async () => {
  await fetchUsername()
})
</script>

<style scoped>

/* Sección de bienvenida */
.welcome-section {
  position: relative;
  background-size: cover;
  background-position: center;
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 20px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6); /* Efecto de oscurecimiento */
  z-index: 1;
}

.welcome-content {
  position: relative;
  z-index: 2;
  color: #ebd2ff;
}

.h1-welcome {
  font-family: Titulo, sans-serif;
  font-size: 3rem;
  margin-bottom: 20px;
}

.h2-welcome {
  font-family: NunitoBlack, sans-serif;
  font-size: 1.5rem;
  margin: 1.5em;
}

/* Sección de información */
.info-section {
  display: flex;
  justify-content: space-around;
  padding: 40px 20px;
  background-color: rgba(19, 14, 43, 0.97);
  border-top: solid 2px;
  border-color: #ff3974;
  flex-wrap: wrap; /* Permite que las tarjetas se vayan hacia abajo en pantallas más pequeñas */
  box-shadow: 0px -10px 5px rgba(249,36,100,1);
}

.info-card {
  background-color: rgba(19, 14, 43, 1);
  text-align: center;
  padding: 1.3em;
  border-radius: 10px;
  width: 22%;
  margin: 0.8em;
  font-family: Titulo, sans-serif;
  box-shadow: -4px 4px 10px rgba(249,36,100,255);
  color: #ebd2ff;
  min-width: 250px; /* Ajusta este valor según el ancho mínimo que quieras para las tarjetas */
}

h2 {
  font-size: 1.5rem;
  word-wrap: break-word; /* Permite que el texto largo se ajuste y no se desborde */
}

p {
  font-family: NunitoBlack !important;
  font-size: 1.2em;
}

/* Estilo de los botones */
.btn-primary {
  font-family: Titulo, sans-serif;
  background-color: #ff8c42;
  border-color: #ff8c42;
}

.btn-primary:hover {
  background-color: rgba(19, 14, 43, 1);
  border-color: #ff6f1f;
  color: #ff6f1f;
  box-shadow: -1px 2px 4px rgba(249,36,100,255);
}

.pruebas {
  position: relative;
  z-index: 100;
}
</style>
