<template>
  <NavHome></NavHome>

  <!-- ---------------------------------------------------------------- -->
  <div class="container">
    <div class="main-body">
      <!-- /Breadcrumb -->

      <div class="row gutters-sm">
        <div class="col-sm-6 mb-3">
          <div class="card h-100">
            <div class="card-body">
              <h6 class="d-flex align-items-center mb-3">Users List</h6>

              <ul class="list-group">
                <li
                  v-for="user in users"
                  :key="user.id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div class="d-flex align-items-center">
                    <span class="status-indicator me-2" :class="getStatusClass(user.status)"></span>
                    <span class="me-2">{{ user.username }}</span>
                  </div>
                  <span class="badge" :class="getBadgeClass(user.status)">
                    {{ getStatusText(user.status) }}
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-sm-6 mb-3">
          <div class="card h-100">
            <div class="card-body">
              <h6 class="d-flex align-items-center mb-3">Friends List</h6>

              <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>
                    <span class="status-indicator bg-success"></span>
                    Jane Smith
                  </span>
                  <span class="badge bg-success">Online</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>
                    <span class="status-indicator bg-danger"></span>
                    Mike Johnson
                  </span>
                  <span class="badge bg-danger">Offline</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>
                    <span class="status-indicator bg-success"></span>
                    Emily Davis
                  </span>
                  <span class="badge bg-success">Online</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>
                    <span class="status-indicator bg-danger"></span>
                    David Brown
                  </span>
                  <span class="badge bg-danger">Offline</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-sm-6 mb-3">
          <div class="card h-100">
            <div class="card-body card-body2">
              <h6 class="d-flex align-items-center mb-3">Player Stats</h6>
              <div class="d-flex flex-column">
                <div class="d-flex justify-content-between mb-3">
                  <span>Victories:</span>
                  <span>123</span>
                </div>
                <div class="d-flex justify-content-between mb-3">
                  <span>Losses:</span>
                  <span>45</span>
                </div>
                <div class="d-flex justify-content-between mb-3">
                  <span>Games Played:</span>
                  <span>168</span>
                </div>
                <div class="d-flex justify-content-between mb-3">
                  <span>Total Points:</span>
                  <span>9876</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <main class="px-3">
    <div>
      <ul>
        <li v-for="user in users" :key="user.id">
          <strong>{{ user.username }}</strong> - {{ user.email }}
        </li>
      </ul>
    </div>
  </main>
</template>

<script setup lang="ts">
import NavHome from './NavHome.vue'
import { ref, onMounted, inject } from 'vue'
const api: Api = inject('$api') as Api

const isEditing = ref(false)
const username = ref('User')
const users = ref([])

// Lifecycle hook similar a `created` en Options API
onMounted(async () => {
  await fetchUsername()
  await fetchUserList()
})

const fetchUsername = async () => {
  try {
    const response = await api.get('whoami')
    username.value = response.username // Reemplazar con la estructura real de tu respuesta
  } catch (error) {
    console.error(
      'Error fetching username:',
      error.response ? error.response.username : error.message
    )
  }
}

const fetchUserList = async () => {
  try {
    const response = await api.get('friendship/users', ['data'])
    users.value = response
  } catch (error) {
    console.error('Error fetching users:', error.response ? error.response.data : error.message)
  }
}

// Define your methods
const getStatusClass = (status) => {
  return {
    'bg-success': status === 'Online',
    'bg-danger': status === 'Offline',
    'bg-warning': status === 'Absent'
  }
}

const getBadgeClass = (status) => {
  return {
    'bg-success': status === 'Online',
    'bg-danger': status === 'Offline',
    'bg-warning': status === 'Absent'
  }
}

const getStatusText = (status) => {
  return status === 'Online' ? 'Online' : status === 'Offline' ? 'Offline' : 'Absent'
}
</script>

<style scoped>
body {
  margin-top: 20px;
  color: #1a202c;
  text-align: left;
  background-color: #e2e8f0;
}

.main-body {
  padding: 15px;
}

.card {
  box-shadow:
    0 1px 3px 0 rgba(0, 0, 0, 0.1),
    0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 0 solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
}

.card-h {
  height: 40em;
}

.card-body {
  flex: 1 1 auto;
  min-height: 1px;
  padding: 1rem;
}

.gutters-sm {
  margin-right: -8px;
  margin-left: -8px;
}

.gutters-sm > .col,
.gutters-sm > [class*='col-'] {
  padding-right: 8px;
  padding-left: 8px;
}

.mb-3,
.my-3 {
  margin-bottom: 1rem !important;
}

.bg-gray-300 {
  background-color: #e2e8f0;
}

.h-100 {
  height: 100% !important;
}

.shadow-none {
  box-shadow: none !important;
}

.friends-section {
  background-color: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.friends-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.friend-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
}

.friend-item:last-child {
  border-bottom: none;
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 10px;
  border-radius: 50%;
}

.online {
  background-color: green;
}

.offline {
  background-color: red;
}

.card-body2 {
  padding: 20px;
}

.d-flex {
  display: flex;
}

.justify-content-between {
  justify-content: space-between;
}

.form-control {
  width: 100%;
  margin-bottom: 10px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  background-color: gray; /* Color predeterminado */
}

.card-title {
  font-size: 1.25rem; /* Tamaño del texto del título */
  font-weight: 500; /* Peso del texto para destacar el título */
}

.list-group-item {
  border: 1px solid #dee2e6; /* Añade borde a los ítems de la lista */
  border-radius: 0.25rem; /* Bordes redondeados */
  margin-bottom: 0.5rem; /* Espacio entre los ítems */
}
</style>
