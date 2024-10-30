<!-- ** FALTA AÑADIR LA PARTE DE LA LISTA DE AMIGOS ** -->
<template>
  <div class="pruebas">
    <NavHome></NavHome>
  </div>
  <div class="container">
    <div class="row gutters-sm my-3">
      
      <!-- CARD DEL USUARIO -->
      <div class="col-md-4 d-flex align-items-stretch user-card-container">
        <div class="user-card w-100 m-3 d-flex justify-content-center">
          <div class="d-flex flex-column justify-content-center align-items-center text-center">
            <h2 class="user-name pb-3 px-3">{{ user.username }}</h2>
            <img :src="user.avatarUrl" alt="User Avatar" class="rounded-circle m-3" width="50%">
            <p class="user-data pt-3 pb-1">{{ user.nickname }}</p>
            <p class="user-data pb-3 pt-1">{{ user.email }}</p>

            <!-- BOTONES PARA EDITAR LA INFORMACION O EL AVATAR -->
            <div>
              <button class="btn background-button mt-3 mx-2" @click="goToEditAvatar">Edit avatar</button>
              <button class="btn border-button mt-3 mx-2" @click="goToEditProfile">Edit profile</button>
            </div>
          </div>
        </div>

      </div>
      <!-- ESTADISTICAS DEL USUARIO -->
      <div class="col-md-8 d-flex stats-container">
          <Stats v-if="userLoaded" :userId="user.id"></Stats>
      </div>
    </div>
    
    <!-- LISTA DE AMIGOS -->
    <FriendList v-if="userLoaded" :userId="user.id" class="friend-list"></FriendList>
  </div>
</template>


<script setup lang="ts">

/* ----- IMPORTS ----- */

import { ref, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router'

import NavHome from './NavHome.vue';
import Stats from './Stats.vue';
import FriendList from './FriendList.vue';
import type Api from '@/utils/Api/Api'
import auth from '../../services/user/services/auth/auth.ts'


/* ----- VARIABLES ----- */

const api: Api = inject('$api') as Api;
const Auth: auth = new auth(api)
const router = useRouter()

const user = ref({
  id: 2,
  username: '',
  email: '',
  nickname: '',
  avatarUrl: '',
  wins: '0',
  losses: '0',
});

const userLoaded = ref(false);
/* ----- FETCH INFORMATION ----- */

/* async function fetchPongData() {
  try {
    const response = await Auth.pongData(user.id);
    // console.log('Data sent successfully:', response.data);
    console.log(response);
  } catch (error) {
    console.error('Error sending data:', error);

    if (error.response) {
      const message = error.response.data.message || 'An error occurred.';
      const errors = error.response.data.errors || {};

      let errorMessage = `Request failed. ${message}`;
      if (Object.keys(errors).length > 0) {
        errorMessage += '\nErrors:\n';
        for (const [field, msgs] of Object.entries(errors)) {
          errorMessage += `${field}: ${msgs.join(', ')}\n`;
        }
      }
      alert(errorMessage);
    } else {
      alert('Request to the backend failed. Please try again later.');
    }
  }
}; */

async function fetchUserData() {
  try {
    const response = await Auth.whoami();
    console.log(response);
    user.value = {
      id: response.id,
      username: response.username,
      email: response.email,
      nickname: response.nickname,
      avatarUrl: ''
    };
      await fetchUserAvatar();

    // Indicar que los datos del usuario han sido cargados
    userLoaded.value = true;
  } catch (error: any) {
    console.error('Error fetching user data:', error.message);
  }
}
async function fetchUserAvatar() {
  try {
    const response = await api.get('auth/get-avatar');
    if (response.status === 200) {
      const avatarBase64 = response.avatar_base64;
      user.value.avatarUrl = `data:image/jpeg;base64,${avatarBase64}`;
    } else {
      console.error('Failed to fetch avatar:', response.data);
    }
  } catch (error) {
    console.error('Error fetching user avatar:', error.message);
  }
}

onMounted(async () => {
  await fetchUserData();
  // await fetchPongData();
});


/* ----- REDIRECCIONES A VISTAS ----- */

const goToEditAvatar = () => {
  router.push('/edit-avatar')
}

const goToEditProfile = () => {
  router.push('/edit-profile')
}

</script>

<style scoped>

.user-name {
  font-family: Titulo !important;
  color:#ebd2ff;
  margin-bottom: 0px;
}

.user-data {
  font-family: NunitoBlack !important;
  color:#ebd2ff;
  margin-bottom: 0px;
  font-size: 1.2em;

}

.stats-container {
  position: relative;
  z-index: 1; /* Mantiene las estadísticas debajo de la tarjeta */
}

.pruebas {
  position: relative;
  z-index: 100;
}
</style>
