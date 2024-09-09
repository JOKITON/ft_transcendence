<template>
  <NavHome></NavHome>

  <!-- ---------------------------------------------------------------- -->
  <div class="container">
    <div class="main-body">


      <!-- /Breadcrumb -->

      <div class="row gutters-sm">
        <div class="col-md-4 mb-3">
          <div class="card">
            <div class="card-body">
              <div class="d-flex flex-column align-items-center text-center">
                <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="Admin" class="rounded-circle"
                  width="150">
                <div class="mt-3">
                  <h4>{{ username }}</h4>
                  <p class="text-secondary mb-1">Full Stack Developer</p>
                  <p class="text-muted font-size-sm">Bay Area, San Francisco, CA</p>
                  <button class="btn btn-primary">Follow</button>
                  <button class="btn btn-outline-primary">Message</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-8">
          <div class="card mb-3">
            <div class="card-body">
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Fullname</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  <span v-if="!isEditing">{{ username }}</span>
                  <input v-else type="text" class="form-control" v-model="user.fullName">
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Email</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  <span v-if="!isEditing">fip@jukmuh.al</span>
                  <input v-else type="email" class="form-control" v-model="user.email">
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Phone</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  <span v-if="!isEditing">(239) 816-9029</span>
                  <input v-else type="text" class="form-control" v-model="user.phone">
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Mobile</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  <span v-if="!isEditing">(320) 380-4539</span>
                  <input v-else type="text" class="form-control" v-model="user.mobile">
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Address</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  <span v-if="!isEditing">Bay Area, San Francisco, CA</span>
                  <input v-else type="text" class="form-control" v-model="user.address">
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-12">
                  <button class="btn btn-info" @click="isEditing ? saveChanges() : toggleEdit()">
                    {{ isEditing ? 'Save' : 'Edit' }}
                  </button>

                </div>
              </div>
            </div>
          </div>

          <div class="row gutters-sm">
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

    </div>
  </div>
  <!-- ---------------------------------------------------------------- -->

</template>

<script setup lang="ts">
import NavHome from './NavHome.vue'
import { ref, onMounted, inject } from 'vue'
const api: Api = inject('$api') as Api;

const isEditing = ref(false);
const username = ref('User')

// Lifecycle hook similar a `created` en Options API
onMounted(async () => {
  await fetchUsername()
})

// Datos originales del usuario (inmutables)
const originalUser = ref({
  fullName: username ? username : '(None)',
  email: 'fip@jukmuh.al',
  phone: '(239) 816-9029',
  mobile: '(320) 380-4539',
  address: 'Bay Area, San Francisco, CA',
});

// Datos editables del usuario
const user = ref({ ...originalUser.value });

function toggleEdit() {
  if (isEditing.value) {
    // Si se estaba en modo edición y se cancela (sin guardar), se restauran los valores originales
    user.value = { ...originalUser.value };
  } else {
    // Si se hace clic en "Edit", se comienza la edición
    user.value = { ...originalUser.value }; // Asegurarse de comenzar con los datos originales
  }
  isEditing.value = !isEditing.value; // Alternar el modo de edición
}

function saveChanges() {
  // Guardar cambios en los datos originales
  originalUser.value = { ...user.value };
  isEditing.value = false; // Salir del modo de edición
}

const fetchUsername = async () => {
  try {
    const response = await api.get('whoami')
    username.value = response.username // Reemplazar con la estructura real de tu respuesta
  } catch (error) {
    console.error('Error fetching username:', error.response ? error.response.username : error.message)
  }
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
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .1), 0 1px 2px 0 rgba(0, 0, 0, .06);
}

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

.gutters-sm>.col,
.gutters-sm>[class*=col-] {
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
</style>