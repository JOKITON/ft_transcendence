<template>
  <div class="w-100 m-3">
    <h2 class="text-center stat-title">Estadisticas</h2>
    <Carousel :itemsToShow="2.2" :wrapAround="true" :transition="500">
      <Slide v-for="item in items" class="shield-shadow">
        <div class="d-flex flex-column stat shield my-3 py-3">
          <h5 class="py-4 stat-data">{{ item.category }}</h5>
          <img :src="item.image" alt="User Avatar" class="py-2" width="50%" />
          <p class="py-4 stat-data">{{ item.value }}</p>
        </div>
      </Slide>
      <template #addons>
        <Pagination class="" />
      </template>
    </Carousel>
  </div>
</template>

<script setup lang="ts">
/* ----- IMPORTS ----- */

import type Api from '@/utils/Api/Api';
import auth from '@/services/auth/auth'
import { useRouter } from 'vue-router';
import { onMounted, ref, inject } from 'vue';
import { Carousel, Slide, Pagination } from 'vue3-carousel';
import avatar from '../../assets/avatars/pepe.png';
import trophy from '../../assets/avatars/trophy.png';
import loose from '../../assets/avatars/loose.png';
import arcade from '../../assets/avatars/arcade.png';
import score from '../../assets/avatars/score.png';
import time from '../../assets/avatars/time.png';
import spike from '../../assets/avatars/spike.png';

const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)

const props = defineProps({
  userId: {
    type: Number,
    required: true
  }
})

const userPongData = ref({
  wins: 0,
  losses: 0,
  total_games: 0,
  avg_score: 0,
  time_played: 0,
  hits: 0
});


interface Item {
  category: string;
  value: number;
  image: string;
};

const items = ref<Item[]>([]);

onMounted(async () => {
  await fetchPongData()
  await updateItems()
})

async function updateItems() {
  items.value = [
    { category: 'Victorias', value: userPongData.value.wins, image: trophy },
    { category: 'Derrotas', value: userPongData.value.losses, image: loose },
    { category: 'Partidas Jugadas', value: userPongData.value.total_games, image: arcade },
    { category: 'Media de puntuacion', value: userPongData.value.avg_score, image: score },
    { category: 'Duracion de Partida', value: userPongData.value.time_played, image: time },
    { category: 'Remates', value: userPongData.value.hits, image: spike },
  ];
}

async function fetchPongData() {
  try {
    const response = await Auth.pongData(props.userId)
    userPongData.value = response
  } catch (error: any) {
    console.error('Error sending data:', error)

    if (error.response) {
      const message = error.response.data.message || 'An error occurred.'
      const errors = error.response.data.errors || {}

      let errorMessage = `Request failed. ${message}`
      if (Object.keys(errors).length > 0) {
        errorMessage += '\nErrors:\n'
        for (const [field, msgs] of Object.entries(errors)) {
          errorMessage += `${field}: ${(msgs as string[]).join(', ')}\n`;
        }
      }
      alert(errorMessage)
    } else {
      alert('Request to the backend failed. Please try again later.')
    }
  }
}
</script>

<style scoped>
.carousel * {
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

.stat-title {
  color: #ebd2ff !important; /*  #ae28f8 #ae28f8 */
  font-family: 'Titulo' !important;
  padding: 0.5em;
  background-color: rgba(19, 14, 43, 0.97);
  box-shadow: -4px 4px 10px rgba(249, 36, 100, 255);
  border-radius: 5px;
}

.shield-shadow {
  filter: drop-shadow(-6px 6px 6px rgb(255, 57, 116, 1));
}

.stat {
  position: relative;
  min-height: 250px;
  width: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 1;
}

.shield {
  color: #fff;
  background: linear-gradient(45deg, rgba(19, 14, 43), rgb(44, 33, 99), #ff3974);
  clip-path: polygon(50% 100%, 0 70%, 0 0, 100% 0, 100% 70%);
  z-index: 2;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border: solid 2px ff3974;
}

.stat-data {
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
  z-index: 1;
}

.carousel__slide--sliding {
  transition: 0.5s ease;
}

:deep(.carousel__pagination-button::after) {
  background-color: rgba(19, 14, 43, 0.9);
}

:deep(.carousel__pagination-button--active::after) {
  background-color: #e74c3c;
}
</style>
