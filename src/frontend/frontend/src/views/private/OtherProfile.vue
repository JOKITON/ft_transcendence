<template>
  <NavHome></NavHome>

  <div class="container">
      <div class="main-body">
          <div class="row gutters-sm">
              <!-- Perfil de Usuario (1/3 del ancho) -->
              <div class="col-md-4 d-flex align-items-stretch">
                  <div class="card w-100">
                      <div class="card-body d-flex flex-column justify-content-center align-items-center text-center">
                          <img :src="user.avatarUrl" alt="User Avatar" class="rounded-circle" width="150">
                          <div class="mt-3">
                              <h4>User Name {{ user.username }}</h4>
                              <p>Alias</p>
                              <p>{{ user.friendsCount }} friends</p>
                              <div class="d-flex justify-content-center w-100 my-3">
                                  <div class="text-center mx-2 text-success">
                                      <div class="fs-4">Win</div>
                                      <div class="fs-5">{{ user.wins }}</div>
                                  </div>
                                  <div class="text-center">
                                      <span class="fs-4">/</span>
                                  </div>
                                  <div class="text-center mx-2 text-danger">
                                      <div class="fs-4">Losses</div>
                                      <div class="fs-5">{{ user.losses }}</div>
                                  </div>
                              </div>
                              <button class="btn btn-primary mx-1">Follow</button>
                              <button class="btn btn-outline-primary">Message</button>
                          </div>
                      </div>
                  </div>
              </div>
              <!-- Estadísticas del Jugador (2/3 del ancho) -->
              <div class="col-md-8 d-flex align-items-stretch">
                <div class="card w-100">
                  <div class="main-body">
                    <Carousel :items-to-show="2.5" :wrap-around="true">
                      <Slide v-for="slide in 10" :key="slide">
                        <div class="carousel__item">
                          <p>Peter</p>
                        </div>
                      </Slide>
                    </Carousel>
                  </div>
                </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import NavHome from './NavHome.vue';
 import avatar from '/src/assets/avatars/pepe.png'
import { Carousel, Navigation, Slide } from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';

export default defineComponent({
name: 'WrapAround',
components: {
  Carousel,
  Slide,
  Navigation,
  NavHome,
},
setup() {
  const route = useRoute();
  const router = useRouter();
  const user = ref({
    username: '',
    avatarUrl: avatar, // Set the avatar URL directly
    friendsCount: 0,
    wins: 0,
    losses: 0,
    totalVictories: 0,
    totalLosses: 0,
    gamesPlayed: 0,
    totalPoints: 0
  });

  /* async function fetchUserProfile() {
    const userId = route.params.id;
    try {
      const response = await fetch(`/api/users/${userId}`);
      user.value = await response.json();
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  }

  onMounted(() => {
    fetchUserProfile();
  }); */

  return {
    user,
  };
}
});
</script>


<style scoped>
body {
margin-top: 20px;
color: #1a202c;
background-color: #e2e8f0;
}

.main-body {
padding: 15px;
}

.card {
background-color: #fff;
border-radius: .25rem;
box-shadow: 0 1px 3px rgba(0, 0, 0, .1), 0 1px 2px rgba(0, 0, 0, .06);
}

.card-body {
padding: 1rem;
}

.gutters-sm {
margin-right: -8px;
margin-left: -8px;
}

.gutters-sm .col,
.gutters-sm [class*=col-] {
padding-right: 8px;
padding-left: 8px;
}

.mb-3 {
margin-bottom: 1rem;
}

.d-flex {
display: flex;
}

.justify-content-between {
justify-content: space-between;
}

.carousel * {
  box-sizing: border-box;
}
.carousel__item {
  min-height: 200px;
  width: 100%;
  background-color: gray;
  color: #fff;
  font-size: 20px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 10px;
}
</style>
