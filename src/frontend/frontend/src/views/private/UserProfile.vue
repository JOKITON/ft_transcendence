<template>
    <NavHome></NavHome>
    <div class="card">
      <h1>Perfil del usuario. ID: {{ userData.id }}</h1>
      <p>Este es el perfil del usuario: {{ userData.username }} </p>
      <p>Correo: {{ userData.email }}</p>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted, ref, inject, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import NavHome from './NavHome.vue';

  const api = inject('$api') as Api;
  
  const route = useRoute()
  
  const userId = ref<number | null>(null)
  const errorMessage = ref<string | null>(null)
  const userData = ref({
  id: '',
  username: '',
  email: '',
});

const loadUserData = async (id: number) => {
  try {
    const response = await api.get(`auth/search-users-id/${id}/`)
    userData.value = response.user_data
  } catch (error) {
    console.error('Error fetching user data:', error)
    errorMessage.value = 'Error al cargar los datos del usuario'
  }
}

// Obtener el ID del usuario desde la URL y realizar la llamada a la API
onMounted(() => {
  userId.value = parseInt(route.params.id, 10)
  if (userId.value) {
    loadUserData(userId.value)
  }
})

// Observar cambios en los parámetros de la ruta
watch(() => route.params.id, (newId) => {
  userId.value = parseInt(newId, 10)
  if (userId.value) {
    loadUserData(userId.value)  // Recargar los datos del nuevo usuario
  }
})
  </script>
  
  <style>
  .card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 0 solid rgba(0, 0, 0, .125);
    border-radius: .25rem;
  }
  </style>
  