<template>
  <NavHome></NavHome>
  <main class="px-3">
    <h1>Hello {{ username }},</h1>
    <p class="lead">
      Cover is a one-page template for building simple and beautiful home pages. Download, edit the
      text, and add your own fullscreen background photo to make it your own.
    </p>
    <p class="lead">
      <a href="" class="btn btn-lg btn-light fw-bold border-white bg-white">Learn more</a>
    </p>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import NavHome from './NavHome.vue'
import auth from '../../services/user/services/auth/auth.ts'
import type Api from '@/utils/Api/Api'
import type { ApiResponse } from '@/utils/Api/ApiResponse'
// Variables reactivas
const isProfileVisible = ref(false)
const isDropdownVisible = ref(false)
const username = ref('User') // Valor por defecto, será actualizado más adelante
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
/*const fetchUsername = async () => {
  try {
    const response = await api.get('user/whoami/', { withCredentials: true })
    username.value = response.data.username // Reemplazar con la estructura real de tu respuesta
  } catch (error) {
    console.error('Error fetching username:', error.response ? error.response.data : error.message)
  }
}*/

api.setAccessToken()
const response: ApiResponse<Record<string, any>> = await api.post<Record<string, any>>('pong/users')

// Función para alternar el menú desplegable
const toggleDropdown = () => {
  isDropdownVisible.value = !isDropdownVisible.value
}

// Funciones de manejo de perfil y configuración
const openSettings = () => {
  alert('Settings clicked')
}

const openProfile = () => {
  alert('Profile clicked')
}

// Lifecycle hook similar a `created` en Options API
onMounted(async () => {
  await response.data.map((user) => new User(user.id, user.username, user.email))
})
</script>
<style>
@import url('https://cdn.jsdelivr.net/npm/@docsearch/css@3');

header {
  background-color: white;
}

main {
  background-color: #343a40;
  color: whitesmoke;
}

.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
}

@media (min-width: 768px) {
  .bd-placeholder-img-lg {
    font-size: 3.5rem;
  }
}

.b-example-divider {
  width: 100%;
  height: 3rem;
  background-color: rgba(0, 0, 0, 0.1);
  border: solid rgba(0, 0, 0, 0.15);
  border-width: 1px 0;
  box-shadow:
    inset 0 0.5em 1.5em rgba(0, 0, 0, 0.1),
    inset 0 0.125em 0.5em rgba(0, 0, 0, 0.15);
}

.b-example-vr {
  flex-shrink: 0;
  width: 1.5rem;
  height: 100vh;
}

.bi {
  vertical-align: -0.125em;
  fill: currentColor;
}

.nav-scroller {
  position: relative;
  z-index: 2;
  height: 2.75rem;
  overflow-y: hidden;
}

.nav-scroller .nav {
  display: flex;
  flex-wrap: nowrap;
  padding-bottom: 1rem;
  margin-top: -1px;
  overflow-x: auto;
  text-align: center;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
}

.btn-bd-primary {
  --bd-violet-bg: #712cf9;
  --bd-violet-rgb: 112.520718, 44.062154, 249.437846;

  --bs-btn-font-weight: 600;
  --bs-btn-color: var(--bs-white);
  --bs-btn-bg: var(--bd-violet-bg);
  --bs-btn-border-color: var(--bd-violet-bg);
  --bs-btn-hover-color: var(--bs-white);
  --bs-btn-hover-bg: #6528e0;
  --bs-btn-hover-border-color: #6528e0;
  --bs-btn-focus-shadow-rgb: var(--bd-violet-rgb);
  --bs-btn-active-color: var(--bs-btn-hover-color);
  --bs-btn-active-bg: #5a23c8;
  --bs-btn-active-border-color: #5a23c8;
}

.bd-mode-toggle {
  z-index: 1500;
}

.bd-mode-toggle .dropdown-menu .active .bi {
  display: block !important;
}
</style>

