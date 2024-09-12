<template>
  <NavHome></NavHome>

  <!-- ---------------------------------------------------------------- -->
  <div class="container">
    <div class="main-body">
      <div class="row gutters-sm">
        <div class="col-md-4 mb-3">
          <div class="card">
            <div class="card-body">
              <div class="d-flex flex-column align-items-center text-center">
                <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="Admin" class="rounded-circle" width="150">
                <button class="btn btn-primary m-3" @click="editImage">Edit image</button>
                <div class="mt-3">
                  <h4>{{ user.username }}</h4>
                  <p class="text-secondary mb-1">Full Stack Developer</p>
                  <p class="text-muted font-size-sm">Bay Area, San Francisco, CA</p>
                  <button class="btn btn-primary m-1">Follow</button>
                  <button class="btn btn-outline-primary m-1">Message</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-8">
          <div class="card mb-3">
            <div class="card-body">
              <form id="profileUpdate" @submit.prevent="saveChanges">
                <!-- Fullname -->
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">User Name</h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    <span v-if="!isEditing">{{ user.username }}</span>
                    <input v-else type="text" class="form-control" v-model="form.username">
                  </div>
                </div>
                <hr>

                <!-- Email -->
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">Email</h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    <span v-if="!isEditing">{{ user.email }}</span>
                    <input v-else type="email" class="form-control" v-model="form.email">
                  </div>
                </div>
                <hr>

                <!-- Nickname -->
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">Nickname</h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    <span v-if="!isEditing">{{ user.nickname }}</span>
                    <input v-else type="text" class="form-control" v-model="form.nickname">
                  </div>
                </div>
                <hr>
              </form>
              <!-- Save or Edit button -->
              <div class="row">
                <div class="col-sm-12">
                  <button class="btn btn-info" @click="isEditing ? saveChanges() : toggleEdit()">
                    {{ isEditing ? 'Save' : 'Edit' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          <!-- Player Stats -->
          <div class="card-md-3">
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
  <!-- ---------------------------------------------------------------- -->
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue';
import NavHome from './NavHome.vue';

const api: Api = inject('$api') as Api;

const isEditing = ref(false);
const user = ref({
  username: 'User',
  email: 'email',
  nickname: 'nickname',
});

const form = ref({
  username: user.value.username,
  email: user.value.email,
  nickname: user.value.nickname,
});

function toggleEdit() {
  if (isEditing.value) {
    // Restores the original values when edit mode is canceled
    form.value = { ...user.value };
  }
  isEditing.value = !isEditing.value;
}

const saveChanges: () => Promise<void> = async () => {
  try {
    const response = await api.post("update-profile",form.value)
    console.log('saved successful ', response)
    window.location.reload();
  } catch (error: any) {
    window.alert('An error occurred while submitting the form')
    console.error('An error occurred while submitting the form:', error)
  }
}

async function fetchUserData() {
  try {
    const response = await api.get('whoami');
    user.value = {
      username: response.username,
      email: response.email,
      nickname: response.nickname,
    };
    form.value = { ...user.value };
  } catch (error: any) {
    console.error('Error fetching user data:', error.message);
  }
}

onMounted(async () => {
  await fetchUserData();
});
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