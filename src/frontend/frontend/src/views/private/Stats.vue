<template>
  <div class="w-100 m-3">
    <h2 class="text-center stat-title">Estadisticas</h2>
    <Carousel :itemsToShow="2.2" :wrapAround="true" :transition="500">
      <Slide v-for="item in items" class="shield-shadow">
        <div class="d-flex flex-column stat shield my-3 py-3">
          <h5 class="py-4 stat-data">{{ item.category }}</h5>
          <img :src="item.image" alt="User Avatar" class="py-2" width="50%">
          <p class="py-4 stat-data">{{ item.value }}</p>
        </div>
      </Slide>
      <template #addons>
        <Pagination class=""/>
      </template>
    </Carousel>
  </div>
</template>

<script setup lang="ts">

/* ----- IMPORTS ----- */

import type Api from '@/utils/Api/Api'
import auth from '../../services/user/services/auth/auth.ts'
import { useRouter } from 'vue-router'
import { onMounted, ref, inject } from 'vue';
import { Carousel, Slide, Pagination } from 'vue3-carousel';
import avatar from '../../assets/avatars/pepe.png';
import img1 from '../../assets/avatars/trofeo.png';
import img2 from '../../assets/avatars/perder.png';
import img3 from '../../assets/avatars/maquina-de-arcade.png';

const api: Api = inject('$api') as Api;
const Auth: auth = new auth(api)
const router = useRouter()

const user = ref({
  id: 2,
  username: '',
});

const userPongData = ref({
  name: '',
  wins: 0,
  losses: 0,
  total_games: 0,
  avg_score: 0,
});

const items = ref([
  { category: 'Victorias', value: '0' , image: ref(img1) },
  { category: 'Derrotas', value: '10', image: ref(img2) },
  { category: 'Partidas Jugadas', value: '10', image: ref(img3) },
  { category: 'Duracion de Partida', value: '10', image: ref(avatar) }
]);

onMounted(async () => {
  await fetchUserData();
  await fetchPongData();
  await updateItems();
});

async function updateItems() {
  items.value = [
    { category: 'Victorias', value: userPongData.value.wins, image: ref(img1) },
    { category: 'Derrotas', value: userPongData.value.losses, image: ref(img2) },
    { category: 'Partidas Jugadas', value: userPongData.value.total_games, image: ref(img3) },
    { category: 'Media de puntuacion', value: userPongData.value.avg_score, image: ref(avatar) },
    { category: 'Duracion de Partida', value: userPongData.value.avg_position, image: ref(avatar) },
  ];
}

async function fetchUserData() {
  try {
    const response = await Auth.whoami();
    user.value = {
      id: response.id,
      username: response.username,
    };
  } catch (error: any) {
    console.error('Error fetching user data:', error.message);
  }
}

async function fetchPongData() {
  try {
    const response = await Auth.pongData(user.value.id);
    // console.log('Data sent successfully:', response.data);
    userPongData.value = response;
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
};

</script>

<style scoped>

.carousel * {
  box-sizing: border-box;
}

.stat-title{
  color: #ebd2ff !important; /*  #ae28f8 #ae28f8 */
  font-family: 'Titulo' !important;
  padding: 0.5em;
  background-color: rgba(19, 14, 43, 0.97);
  box-shadow: -4px 4px 10px rgba(249,36,100,255);
  border-radius: 5px;
}

.shield-shadow{
  filter: drop-shadow(-6px 6px 6px  rgb(255, 57, 116, 1));
}

.stat {
  position: relative;
  min-height: 250px;
  width: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.shield {
  color: #fff;
  background: linear-gradient(45deg,rgba(19, 14, 43), rgb(44, 33, 99), #ff3974);
  clip-path: polygon(50% 100%, 0 70%, 0 0, 100% 0, 100% 70%);
  z-index: 2;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border: solid 2px ff3974;
}

.stat-data{
  font-size: 1.3em;
  font-family: 'NunitoBlack' !important;
  color: #ebd2ff;
}

.carousel__slide {
  opacity: 0.9;
  transform: scale(0.8);
  padding-bottom: 0.5em;
  padding-top: 1em;
}

.carousel__slide--prev {
  opacity: 0.9;
  transform: scale(0.8);
}

.carousel__slide--next {
  opacity: 0.9;
  transform: scale(0.8);
}

.carousel__slide--active {
  opacity: 1;
  transform: scale(1);
}

.carousel__slide--sliding {
  transition: 0.5s ease;
}

::v-deep .carousel__pagination-button::after {
  background-color:rgba(19, 14, 43, 0.9);
}

::v-deep .carousel__pagination-button--active::after {
  background-color: #e74c3c;
}

</style>