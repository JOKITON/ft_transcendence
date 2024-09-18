<template>
  <header class="p-3 mb-3 border-bottom">
    <div class="container">
      <div
        class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"
      >
        <a
          href="/"
          class="d-flex align-items-center mb-2 mb-lg-0 link-body-emphasis text-decoration-none"
        >
          <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap">
            <use xlink:href="#bootstrap"></use>
          </svg>
        </a>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li>
            <router-link class="nav-link px-2 link-secondary" to="/home">Home</router-link>
          </li>
          <li><router-link class="nav-link px-2 link-secondary" to="/pong">Pong</router-link></li>
          <li class="nav-link px-2 link-secondary">
            <a
              @click="toggleDropdownAdmin"
              class="d-block link-body-emphasis text-decoration-none dropdown-toggle"
              >Admin</a
            >
            <div class="dropdown text-end">
              <ul class="dropdown-menu text-small" :class="{ show: isDropdownAdminVisible }">
                <li>
                  <router-link class="nav-link px-2 link-secondary" to="/user-list"
                    >User List</router-link
                  >
                </li>
                <li>
                  <hr class="dropdown-divider" />
                </li>
                <li><a class="dropdown-item">Add something here</a></li>
              </ul>
            </div>
          </li>
        </ul>

        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search">
          <input type="search" class="form-control" placeholder="Search..." aria-label="Search" />
        </form>

        <p class="d-block link-body-emphasis text-decoration-none">{{ username }}</p>
        <div class="dropdown text-end">
          <a
            @click="toggleDropdownSettings"
            class="d-block link-body-emphasis text-decoration-none dropdown-toggle"
          >
            <img
              src="https://avatars.githubusercontent.com/u/99480973?v=4"
              alt="mdo"
              class="rounded-circle"
              width="32"
              height="32"
            />
          </a>
          <ul class="dropdown-menu text-small" :class="{ show: isDropdownSettingsVisible }">
            <li><a @click="openSettings" class="dropdown-item">Settings</a></li>
            <li><a @click="openProfile" class="dropdown-item">Profile</a></li>
            <li><a @click="openFriends" class="dropdown-item">Friends</a></li>
            <li>
              <hr class="dropdown-divider" />
            </li>
            <li><a @click="logoutUser" class="dropdown-item">Sign out</a></li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import type Api from '../../services/Api/api'
import auth from '../../services/user/services/auth/auth'

const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)
// Variables reactivas
const isProfileVisible = ref(false)
const isDropdownSettingsVisible = ref(false)
const isDropdownAdminVisible = ref(false)
const username = ref('User') // Valor por defecto, será actualizado más adelante

const router = useRouter()

// Función para cerrar sesión
const logoutUser = async () => {
  try {
    const response: boolean = await Auth.logout()
    console.log('Logout successful:', response.data)
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error.response ? error.response.data : error.message)
    alert('Logout failed. ' + (error.response ? error.response.data.message : error.message))
  }
}

// Función para obtener el nombre de usuario
const fetchUsername = async () => {
  try {
    const response = await Auth.whoami()
    username.value = response.username // Reemplazar con la estructura real de tu respuesta
  } catch (error) {
    console.error('Error fetching username:', error.response ? error.response.data : error.message)
  }
}

// Función para obtener el nombre de usuario
const fetchFriendList = async () => {
  try {
    const response = await api.get('friend-list')
    username.value = response.username // Reemplazar con la estructura real de tu respuesta
  } catch (error) {
    console.error('Error fetching username:', error.response ? error.response.data : error.message)
  }
}

// Funciones para alternar los menús desplegables
const toggleDropdownSettings = () => {
  isDropdownSettingsVisible.value = !isDropdownSettingsVisible.value
}

const toggleDropdownAdmin = () => {
  isDropdownAdminVisible.value = !isDropdownAdminVisible.value
}

// Funciones de manejo de perfil y configuración
const openSettings = () => {
  router.push('/other-profile')
}

const openProfile = () => {
  router.push('/profile')
}

const openFriends = () => {
  router.push('/friends')
}
// Lifecycle hook similar a `created` en Options API
onMounted(async () => {
  await fetchUsername()
})
</script>
<style></style>
