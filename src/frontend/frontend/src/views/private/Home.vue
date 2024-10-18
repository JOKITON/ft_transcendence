<template>
  <div class="pruebas">
    <NavHome></NavHome>
  </div>
  <main class="home-wrapper">
    <!-- Sección de bienvenida con el tema de Pong -->
    <section class="welcome-section">
      <div class="overlay"></div>
      <div class="welcome-content">
        <h1>Welcome to Magic Super Mega Pong, {{ username }}</h1>
        <p>Challenge yourself and compete with players from around the world.</p>
        <button @click="goToPong" class="btn btn-lg btn-primary">Start Playing</button>
      </div>
    </section>

    <!-- Sección de información personalizada -->
    <section class="info-section">
      <div class="info-card">
        <div class="icon">
          <i class="fas fa-gamepad"></i>
        </div>
        <h2>Play a Game</h2>
        <p>Jump into a match and test your skills.</p>
        <button @click="goToPong" class="btn btn-outline-light">Play Now</button>
      </div>
      <div class="info-card">
        <div class="icon">
          <i class="fas fa-user-friends"></i>
        </div>
        <h2>Challenge Friends</h2>
        <p>Invite your friends and see who comes out on top.</p>
        <button @click="goToFriends" class="btn btn-outline-light">Challenge Friends</button>
      </div>
      <div class="info-card">
        <div class="icon">
          <i class="fas fa-cog"></i>
        </div>
        <h2>Profile Settings</h2>
        <p>Customize your avatar and update your profile information.</p>
        <button @click="goToSettings" class="btn btn-outline-light">Edit Profile</button>
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
.home-wrapper {
  font-family: 'Nunito', sans-serif;
  color: #ffffff;
}

/* Sección de bienvenida */
.welcome-section {
  position: relative;
  background-image: url('https://your-background-image-url.jpg'); /* Cambia por tu imagen */
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
}

.welcome-content h1 {
  font-family: Titulo, sans-serif;
  font-size: 3rem;
  margin-bottom: 20px;
}

.welcome-content p {
  font-family: Titulo, sans-serif;
  font-size: 1.2rem;
  margin-bottom: 30px;
}

.welcome-content button {
  font-family: Titulo, sans-serif;
  font-size: 1.1rem;
  padding: 10px 30px;
  cursor: pointer;
}

/* Sección de información */
.info-section {
  display: flex;
  justify-content: space-around;
  padding: 40px 20px;
  background-color: #223d5a;
  flex-wrap: wrap;
}

.info-card {
  background-color: #2c506f;
  text-align: center;
  padding: 20px;
  border-radius: 10px;
  width: 22%;
  margin: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.info-card .icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.info-card h2 {
  font-family: Titulo, sans-serif;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.info-card p {
  font-family: Titulo, sans-serif;
  margin-bottom: 20px;
}

.info-card button {
  font-family: Titulo, sans-serif;
  font-size: 1rem;
  padding: 8px 20px;
  color: #ffffff;
  border: 1px solid #ffffff;
  background-color: transparent;
  cursor: pointer;
}

.info-card button:hover {
  background-color: #ffffff;
  color: #223d5a;
}

.play-card .icon {
  color: #28a745; /* Verde para el icono de juego */
}

.play-card button {
  font-family: Titulo, sans-serif;
  background-color: #28a745;
  border-color: #28a745;
}

.play-card button:hover {
  background-color: #218838;
  border-color: #218838;
}

/* Estilo de los botones */
.btn-primary {
  font-family: Titulo, sans-serif;
  background-color: #ff8c42;
  border-color: #ff8c42;
}

.btn-primary:hover {
  background-color: #ff6f1f;
  border-color: #ff6f1f;
}

.pruebas {
  position: relative;
  z-index: 100;
}
</style>
