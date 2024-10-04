<template>
  <NavHome></NavHome>
  <div class="container">
      <div class="row gutters-sm my-3">
        <div class="col-md-4 d-flex align-items-stretch">
          <div class="user-card w-100 m-3 d-flex justify-content-center">
            <div class="d-flex flex-column justify-content-center align-items-center text-center">
              <h2 class="user-name pb-3 px-3">{{ userData.username }}</h2>
              <img :src="userData.avatar" alt="User Avatar" class="rounded-circle py-3" width="50%">
              <p class="user-alias py-3">{{ userData.nickname }}</p>

              <!-- BOTONES PARA EDITAR LA INFORMACION O EL AVATAR -->
              <div>
                <button class="btn background-button mt-3 mx-2">Follow</button>
                <button class="btn border-button mt-3 mx-2">Message</button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-8 d-flex">
            <MyCarousel></MyCarousel>
        </div>
      </div>
    <FriendList v-if="userLoaded" :userId="userData.id"></FriendList>
  </div>
</template>


<script setup lang="ts">

import { onMounted, ref, inject, watch } from 'vue';
import { useRoute } from 'vue-router';
import NavHome from './NavHome.vue';
import MyCarousel from './Stats.vue';
import FriendList from './FriendList.vue';
import avatar from '../../assets/avatars/pepe.png';


/* ----- VARIABLES ----- */

const api = inject('$api') as Api;
const route = useRoute()

const userId = ref<number | null>(null)
const errorMessage = ref<string | null>(null)

const userData = ref({
id: '',
username: '',
nickname: '',
email: '',
avatar: '',
});

const userLoaded = ref(false);
/* ----- CARGAR DATOS USUARIO POR ID ----- */

const fetchUserData = async (id: number) => {
  try {
    const response = await api.get(`auth/search-user-id/${id}/`)
    console.log(response)
    userData.value = {
      id: response.user_data.id,
      username: response.user_data.username,
      nickname: response.user_data.nickname,
      email: response.user_data.email,
      avatar: response.user_data.avatar,
    };
    userData.value.avatar = '/src/assets/' + userData.value.avatar;
    userLoaded.value = true;
  } catch (error) {
    console.error('Error fetching user data:', error)
    errorMessage.value = 'Error al cargar los datos del usuario'
  }
}

const fetchUserAvatar = async (id: number) => {
  try {
    const response = await api.get(`auth/get-avatar-id/${id}/`);
    if (response.status === 200) {
      const avatarBase64 = response.avatar_base64;
      userData.value.avatar = `data:image/jpeg;base64,${avatarBase64}`;
    } else {
      console.error('Failed to fetch avatar:', response.data);
    }
  } catch (error) {
    console.error('Error fetching user avatar:', error.message);
  }
}
/* ----- CARGAR DATOS USUARIO POR ID ----- */

// Observar cambios en los parámetros de la ruta
watch(() => route.params.id, (newId) => {
  userId.value = parseInt(newId, 10)
  if (userId.value) {
    fetchUserData(userId.value)  // Recargar los datos del nuevo usuario
    fetchUserAvatar(userId.value)
  }
})


// Obtener el ID del usuario desde la URL y realizar la llamada a la API
onMounted(() => {
  userId.value = parseInt(route.params.id, 10)
  if (userId.value) {
    fetchUserData(userId.value)
    fetchUserAvatar(userId.value)
  }
})

</script>
  
  
<style scoped>

.user-alias {
  font-family: NunitoBlack !important;
  color:#ebd2ff;
  margin-bottom: 0px;
  font-size: 1.2em;
}
  
.user-name {
  font-family: Titulo !important;
  color:#ebd2ff;
  margin-bottom: 0px;
}

</style>