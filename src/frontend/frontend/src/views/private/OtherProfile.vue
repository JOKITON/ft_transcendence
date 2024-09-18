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
                                <h4>User Name{{ user.username }}</h4>
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
                        <div class="card-body">
                            <h6 class="mb-3">Player Stats</h6>
                            <div class="d-flex flex-column">
                                <div class="d-flex justify-content-between mb-3 mt-3">
                                    <span>Victories:</span>
                                    <span>{{ user.totalVictories }}</span>
                                </div>
                                <div class="d-flex justify-content-between mb-3 mt-2">
                                    <span>Losses:</span>
                                    <span>{{ user.totalLosses }}</span>
                                </div>
                                <div class="d-flex justify-content-between mb-3 mt-2">
                                    <span>Games Played:</span>
                                    <span>{{ user.gamesPlayed }}</span>
                                </div>
                                <div class="d-flex justify-content-between mb-3 mt-2">
                                    <span>Total Points:</span>
                                    <span>{{ user.totalPoints }}</span>
                                </div>
                                <div class="d-flex justify-content-between mb-3 mt-2">
                                    <span>Total Points:</span>
                                    <span>{{ user.totalPoints }}</span>
                                </div>

                                <div class="d-flex justify-content-between mb-3 mt-2">
                                    <span>Total Points:</span>
                                    <span>{{ user.totalPoints }}</span>
                                </div>
                                <div class="d-flex justify-content-between mb-3 mt-2">
                                    <span>Total Points:</span>
                                    <span>{{ user.totalPoints }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <section class="pt-5 pb-5">
        <div class="container">
            <div class="row">
                <div class="col-6">
                    <h3 class="mb-3">Multi Item Carousel cards</h3>
                </div>
                <div class="col-6 text-right">
                    <a class="btn btn-primary mb-3 mr-1" 
                       href="#carouselExampleIndicators2"
                       role="button"
                        data-slide="prev">
                        <i class="fa fa-arrow-left"></i>
                    </a>
                    <a class="btn btn-primary mb-3"
                       href="#carouselExampleIndicators2"
                       role="button"
                       data-slide="next">
                        <i class="fa fa-arrow-right"></i>
                    </a>
                </div>
                <div class="col-12">
                    <div id="carouselExampleIndicators2" 
                         class="carousel slide"
                         data-ride="carousel">

                        <div class="carousel-inner">
                            <div class="carousel-item active">
                                <div class="row">

                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" 
                                                 alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20240122184958/images2.jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">
                                                  Special title treatment</h4>
                                                <p class="card-text">With supporting text
                                                                       below as a natural lead-in</p>

                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" 
                                                 alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20240122184958/images2.jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">Special title
                                                                         treatment</h4>
                                                <p class="card-text">With supporting 
                                                                       text below as a natural
                                                                       lead-in to additional 
                                                                       content.</p>

                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" 
                                                 alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20230407154213/gfg-bag.jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">Special title treatment</h4>
                                                <p class="card-text">With supporting text below
                                                                       as a natural lead-in to
                                                                     additional content.</p>

                                            </div>
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="carousel-item">
                                <div class="row">

                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" 
                                                 alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20240110011854/reading-925589_640.jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">Special title treatment</h4>
                                                <p class="card-text">With supporting text below 
                                                                      as a natural lead-in to
                                                                    additional content.</p>

                                            </div>

                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20240122182422/images1.jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">Special title treatment</h4>
                                                <p class="card-text">With supporting text below 
                                                                       as a natural lead-in to
                                                                        additional content.</p>

                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20240110011854/reading-925589_640.jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">Special title treatment</h4>
                                                <p class="card-text">With supporting text below 
                                                                      as a natural lead-in to
                                                                       additional content.</p>

                                            </div>
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="carousel-item">
                                <div class="row">

                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" 
                                                 alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20240110011815/sutterlin-1362879_640-(1).jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">Special title treatment</h4>
                                                <p class="card-text">With supporting text below 
                                                                      as a natural lead-in to
                                                                    additional content.</p>

                                            </div>

                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20240110011929/glasses-1052010_640.jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">Special title treatment</h4>
                                                <p class="card-text">With supporting text below
                                                                       as a natural lead-in to 
                                                                        additional content.</p>

                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card">
                                            <img class="img-fluid" 
                                                 alt="100%x280"
                                                src=
"https://media.geeksforgeeks.org/wp-content/uploads/20240110011929/glasses-1052010_640.jpg">
                                            <div class="card-body">
                                                <h4 class="card-title">Special title treatment</h4>
                                                <p class="card-text">With supporting text below 
                                                                       as a natural lead-in to
                                                                     additional content.</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
        </div>
    </div>
</template>



<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import NavHome from './NavHome.vue';
import avatar from './pepe.png'

const route = useRoute();
const router = useRouter();
const user = ref({
  username: '',
  avatarUrl: ref(avatar),
  friendsCount: 0,
  wins: 0,
  losses: 0,
  totalVictories: 0,
  totalLosses: 0,
  gamesPlayed: 0,
  totalPoints: 0
});

async function fetchUserProfile() {
  const userId = route.params.id; // Assuming the user ID is in the route parameters
  try {
    const response = await fetch(`/api/users/${userId}`);
    user.value = await response.json();
  } catch (error) {
    console.error('Error fetching user profile:', error);
  }
}

onMounted(() => {
  fetchUserProfile();
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
</style>