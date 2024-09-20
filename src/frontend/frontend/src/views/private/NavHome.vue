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
        <!-- @submit.prevent con dudas de si hace falta. @submit es un evento de Vue que captura el envío del formulario. prevent evita que el formulario realice un recargo de página (el comportamiento predeterminado en HTML). Esto es importante porque la búsqueda se maneja dinámicamente con JavaScript sin refrescar la página. -->
        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search" @submit.prevent>
          <!-- 
          v-model="searchQuery": v-model vincula el valor del campo de entrada (<input>) a la variable reactiva searchQuery en el componente de Vue. Cada vez que el usuario escribe algo en el campo, searchQuery se actualiza automáticamente con ese valor.
          @input="performSearch": El evento @input se dispara cada vez que el usuario escribe en el campo. Llama a la función performSearch, que se encargará de realizar la búsqueda en tiempo real
          -->
          <input type="search" class="form-control" placeholder="Search..." aria-label="Search" v-model="searchQuery" @input="performSearch"/>
          <!-- v-if="searchResults.length": Muestra la lista solo si searchResults contiene al menos un elemento. Esto evita que la lista se muestre cuando no hay resultados.

          class="list-group position-absolute":

              list-group: Clase de Bootstrap que agrupa los elementos de la lista para darle un estilo consistente.
              position-absolute: Posiciona la lista de resultados de manera flotante sobre otros elementos para que aparezca justo debajo del campo de búsqueda.

          v-for="user in searchResults": Un bucle que itera sobre cada usuario dentro de searchResults (los resultados de la búsqueda). Cada usuario se representa con un li.

          :key="user.id": En Vue, es una práctica recomendada asignar un key único a cada elemento cuando usas v-for. En este caso, se usa user.id como clave única.

          @click="goToUserProfile(user.id)": El evento @click se dispara cuando el usuario hace clic en un resultado. Llama a la función goToUserProfile y pasa el id del usuario seleccionado como parámetro, lo que redirigirá al perfil de ese usuario.

          class="list-group-item list-group-item-action":

              list-group-item: Estilo de Bootstrap para cada elemento de la lista.
              list-group-item-action: Añade un efecto de "clic" al elemento para indicar que es interactivo.

          {{ user.username }}: Muestra el nombre de usuario de cada resultado de búsqueda. 
          -->
          <ul v-if="searchResults.length" class="list-group position-absolute">
            <li v-for="user in searchResults" :key="user.id" @click="goToUserProfile(user.id)" class="list-group-item list-group-item-action">
              {{ user.username }}
            </li>
          </ul>
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
            <li><a @click="openUsers" class="dropdown-item">Users</a></li>
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

interface User {
  id: number
  username: string
}

const searchQuery = ref<string>('')  // Definimos el tipo como string
const searchResults = ref<User[]>([])  // La búsqueda retorna un array de objetos de tipo User

// Función para realizar la búsqueda
const performSearch = async (): Promise<void> => {
  if (searchQuery.value.length > 0) {
    try {
      const response = await api.get(`auth/search-users?q=${searchQuery.value}`)
      console.log(response)
      searchResults.value = response.user_list // Se asignan los resultados de la búsqueda al array de usuarios
    } catch (error: any) {
      console.error('Error searching users:', error)
    }
  } else {
    searchResults.value = []  // Si no hay búsqueda, vaciamos los resultados
  }
}

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
    const response = await api.get('auth/whoami')
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
  alert('Settings clicked')
}

const openProfile = () => {
  router.push('/profile')
}

const openFriends = () => {
  router.push('/friends')
}

const goToUserProfile = (userId: number) => {
  searchResults.value = []  // Limpiar la lista de resultados
  router.push(`/user-profile/${userId}`)
}

// Lifecycle hook similar a `created` en Options API
onMounted(async () => {
  await fetchUsername()
})
</script>
<style></style>
