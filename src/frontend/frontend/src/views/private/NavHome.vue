<template>
  <header class="p-3 nav-background">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">

        <!-- PAGINAS PRINCIPALES NAV -->
        <ul class="nav col-lg-auto me-lg-auto mb-md-0 nav-flex">
          <li>
            <img src="../../assets/images/logoPong.png" class="d-inline-block mylogo align-top" />
          </li>
          <li><a @click="goToHome" class="nav-link px-4 nav-item">Home</a></li>
          <li><a @click="goToPong" class="nav-link px-4 nav-item">Pong</a></li>

          <!-- DROPDOWN MENU ADMIN -->
<!--           <li class="nav-link px-4">
            <div class="dropdown text-end">
              <a @click="toggleDropdownAdmin" class="d-block text-decoration-none dropdown-toggle nav-item">Admin</a>
              <ul class="dropdown-menu text-small nav-drop" :class="{ show: isDropdownAdminVisible }">
                <li><a @click="openUserList" class="dropdown-item nav-drop-item">User List</a></li>
                <li><a @click="openUserList" class="dropdown-item nav-drop-item">Otra cosa mas</a></li>
              </ul>
            </div>
          </li> -->
        </ul>

        <!-- BUSCADOR -->
        <form class="col-lg-auto mb-lg-0 me-lg-3" role="search" @submit.prevent>
          <input type="search" class="form-control nav-form" placeholder="¿Hay un amigo en ti?" aria-label="Search"
            v-model="searchQuery" @input="performSearch" />
          <ul v-if="searchResults.length" class="list-group position-absolute">
            <li v-for="user in searchResults" :key="user.id" @click="goToUserProfile(user.id)"
              class="list-group-item list-group-item-action">
              {{ user.username }}
            </li>
          </ul>
        </form>

        <!-- NOMBRE DE USUARIO Y DROPDOWN MENU -->
        <a @click="goToProfile" class="nav-link px-4 nav-item">{{ user.username }}</a>
        <div class="dropdown text-end">
          <a @click="toggleDropdownSettings" class="d-block text-decoration-none dropdown-toggle nav-item">
            <img :src="user.avatarUrl" alt="mdo" class="rounded-circle mx-1" width="26" height="26" />
          </a>
          <ul class="dropdown-menu text-small nav-drop" :class="{ show: isDropdownSettingsVisible }">
            <li><a @click="goToSettings" class="dropdown-item nav-drop-item">Settings</a></li>
            <li><a @click="goToProfile" class="dropdown-item nav-drop-item">Profile</a></li>
            <li><a @click="goToFriends" class="dropdown-item nav-drop-item">Friends</a></li>
            <li>
              <hr class="nav-divider" />
            </li>
            <li><a @click="logoutUser" class="dropdown-item nav-sign-out">Sign out</a></li>
          </ul>
        </div>
        <div class="position-relative">
          <a @click="toggleDropdownNotifications" class="d-block text-decoration-none">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-bell"
              viewBox="0 0 16 16">
              <path
                d="M8 16a2 2 0 0 0 1.985-1.75H6.015A2 2 0 0 0 8 16zm.104-14a5.502 5.502 0 0 1 4.396 8.418c-.319.42-.34.682-.39 1.32a.663.663 0 0 1-.696.662H4.586a.663.663 0 0 1-.696-.662c-.05-.638-.071-.9-.39-1.32A5.502 5.502 0 0 1 8.104 2zm3.9 9.4c.306-.44.601-1.025.601-1.78a4.502 4.502 0 0 0-9.004 0c0 .755.295 1.34.601 1.78H3.9l-.002.001c-.042.062-.098.146-.164.258-.157.259-.376.688-.376 1.44h10c0-.752-.219-1.18-.376-1.439a1.007 1.007 0 0 1-.163-.259L12.004 11.4H12z" />
            </svg>
            <!-- Mostrar badge si hay notificaciones nuevas -->
            <span v-if="unreadNotifications > 0"
              class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
              {{ unreadNotifications }}
            </span>
          </a>
          <!-- Desplegable de notificaciones -->
          <ul class="dropdown-menu text-small nav-drop" :class="{ show: isDropdownNotificationsVisible }">
            <li v-if="friendRequests.length === 0" class="dropdown-item nav-drop-item">No new friend requests</li>
            <li v-for="request in friendRequests" :key="request.id" class="dropdown-item nav-drop-item" @click="goToFriends">
              <span v-if="request.friend">
                <strong>{{ request.friend.username }}</strong> has sent you a friend request
              </span>
              <span v-else>
                Unknown user has sent you a friend request
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </header>
  <ChatDropdown />

</template>

<script setup lang="ts">

/* ----- IMPORTS ----- */

import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import type Api from '../../services/Api/api'
import auth from '../../services/user/services/auth/auth'
import ChatDropdown from './DesplegableChat.vue';
import Friendss from './Friends.vue';



/* ----- VARIABLES ----- */

const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)
const router = useRouter()
const searchQuery = ref<string>('')  // Definimos el tipo como string
const searchResults = ref<User[]>([])  // La búsqueda retorna un array de objetos de tipo User
const username = ref('User') // Valor por defecto, será actualizado más adelante
const user = ref({
  username: '',
  avatarUrl: '',
});
const unreadNotifications = ref(0);
const friendRequests = ref([{ id: 1, username: 'JohnDoe' }, { id: 2, username: 'JaneSmith' }]);


/* ----- VARIABLES REACTIVAS ----- */

const isProfileVisible = ref(false)
const isDropdownSettingsVisible = ref(false);
const isDropdownNotificationsVisible = ref(false);
const isDropdownAdminVisible = ref(false);

/* ----- INTERFACES ----- */

interface User {
  id: number
  username: string
}

interface FriendRequest {
  id: number;
  friend: {
    username: string;
    email: string;
  };
}

interface FriendRequestsResponse {
  pending_requests: FriendRequest[];
}


/* ----- BUSCAR USUARIO ----- */

const performSearch = async (): Promise<void> => {
  if (searchQuery.value.length > 0) {
    try {
      const response = await api.get(`auth/search-users?q=${searchQuery.value}`)
      if (response.status === 200) {
        searchResults.value = response.user_list
      } else {
        window.alert(response.message)
        searchQuery.value = "";
        searchResults.value = []
      }
    } catch (error: any) {
      console.error('Error searching users:', error)// ????
      window.alert("Error searching users")
      searchQuery.value = "";
      searchResults.value = []
    }
  } else {
    searchResults.value = []
  }
}


/* ----- CERRAR SESION ----- */

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


/* ----- FETCH INFORMATION ----- */

async function fetchUsername() {
  try {
    const response = await Auth.whoami();
    user.value = {
      username: response.username,
      avatarUrl: response.avatar ? response.avatar : 'avatars/pepe.png',
    };
    user.value.avatarUrl = '/src/assets/' + user.value.avatarUrl;
    // console.log(user.value.avatarUrl )

    // Check if avatarUrl is set to the default '/src/assets/avatars/pepe.png'
    if (user.value.avatarUrl === '/src/assets/avatars/pepe.png') {
      // Use the default local avatar
    } else {
      // Retrieve avatar from the backend
      await fetchUserAvatar();
    }
  } catch (error: any) {
    console.error('Error fetching user data:', error.message);
  }
}

async function fetchUserAvatar() {
  try {
    const response = await api.get('auth/get-avatar');
    if (response.status === 200) {
      const avatarBase64 = response.avatar_base64;
      user.value.avatarUrl = `data:image/jpeg;base64,${avatarBase64}`; // Set the Base64 image as the src
    } else {
      console.error('Failed to fetch avatar:', response.data);
    }
  } catch (error) {
    console.error('Error fetching user avatar:', error.message);
  }
}


/* ----- MENUS DESPLEGABLES ----- */

const toggleDropdownSettings = () => {
  isDropdownSettingsVisible.value = !isDropdownSettingsVisible.value
}

const toggleDropdownAdmin = () => {
  isDropdownAdminVisible.value = !isDropdownAdminVisible.value
}
const toggleDropdownNotifications = () => {
  isDropdownNotificationsVisible.value = !isDropdownNotificationsVisible.value;
  // Marcar notificaciones como leídas
  unreadNotifications.value = 0;
}

/* ----- REDIRECCIONES A VISTAS ----- */

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
const openUserList = () => {
  router.push('/user-list')
}
const goToUserProfile = (userId: number) => {
  searchResults.value = []
  router.push(`/user-profile/${userId}`)
}

onMounted(async () => {

  await fetchUsername()
  await fetchFriendRequests();
})


const acceptFriendRequest = async (requestId: number) => {
  try {
    await api.post('friendship/acceptFriendReq', { request_id: requestId });
    console.log(`Friend request ${requestId} accepted`);
    await fetchFriendRequests();
  } catch (error) {
    console.error('Error accepting friend request', error);
  }
};

const declineFriendRequest = async (requestId: number) => {
  try {
    await api.post('friendship/rejectFriendReq', { request_id: requestId });
    console.log(`Friend request ${requestId} declined`);
    await fetchFriendRequests();
  } catch (error) {
    console.error('Error declining friend request', error);
  }
};

const fetchFriendRequests = async () => {
  try {
    const response = await api.get<FriendRequestsResponse>('friendship/pendingReq');
    friendRequests.value = response.pending_requests || [];
    unreadNotifications.value = friendRequests.value.length;
  } catch (error: any) {
    console.error('Error fetching friend requests:', error.message);
  }
}
/* ----- REVISAR ----- */

/* const fetchFriendList = async () => {
  try {
    const response = await api.get('friend-list')
    username.value = response.username // Reemplazar con la estructura real de tu respuesta
  } catch (error) {
    console.error('Error fetching username:', error.response ? error.response.data : error.message)
  }
} */

</script>

<style scoped>
.nav-drop {
  background-color: rgb(19, 14, 43) !important;
  padding-bottom: 0px !important;
  padding-top: 5px !important;
  margin-top: 17px !important;
}

.mylogo {
  width: 50px;
  height: 50px;
}

.nav-drop-item {
  color: #ebd2ff !important;
  font-family: 'NunitoBlack' !important;
  font-size: 1em !important;
}

.nav-drop-item:hover {
  background-color: #f92464 !important;
}

.nav-form {
  background-color: #ebd2ff !important;
  border: none !important;
  outline: none !important;
  font-family: 'Nunito' !important;
  color: #4e2a61 !important;
}

.nav-form:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.nav-form::placeholder {
  color: #6d3c88 !important;
  opacity: 0.8;
  font-family: 'NunitoItalic' !important;
}

.nav-divider {
  background-color: rgb(206, 29, 82) !important;
  height: 3px;
  margin: 5px 0px;
  border: none;
  opacity: 1 !important;
  box-shadow: 0px 3px 6px rgba(249, 36, 100, 255);
}

.nav-sign-out {
  color: #ebd2ff !important;
  font-family: 'Titulo' !important;
  font-size: 1.em !important;
}

.nav-sign-out:hover {
  background-color: #f92464 !important;
}

ChatDropdown {
  position: fixed; /* Esto lo hace fijo en la pantalla */
  bottom: 20px; /* Ubicación desde la parte inferior de la ventana */
  right: 20px; /* Ubicación desde la parte derecha de la ventana */
  z-index: 10000; /* Elevamos el chat por encima del resto del contenido */
  width: 300px; /* Ajusta el ancho del chat según sea necesario */
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* Opcional: sombra para dar un efecto de elevación */
}

/* Estilo opcional para el botón desplegable del chat */
.chat-button {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 10001; /* Botón por encima del resto */
}
</style>