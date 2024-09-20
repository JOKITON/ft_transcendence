<template>
  <NavHome></NavHome>

  <!-- ---------------------------------------------------------------- -->
  <div class="container">
    <div class="main-body">
      <div class="row gutters-sm d-flex align-items-stretch">
        <div class="col-md-4 my-auto">
          <div class="card">
            <div class="card-body h-100">
              <div class="d-flex flex-column align-items-center text-center">
                <img :src="user.avatarUrl" alt="User Avatar" class="rounded-circle" width="150">
                <button class="btn btn-primary m-3" @click="goToChangeAvatar">Edit image</button>
                <!-- File Input for Avatar Upload -->
                <!--<input type="file" @change="onFileChange" class="form-control-file" accept="image/*" />-->
                <div class="mt-3">
                  <h4>{{ user.username }}</h4>
                  <p>0 friends</p>
                  <div class="d-flex justify-content-center w-100 my-3">
                    <div class="text-center mx-2 text-success">
                      <div class="fs-4">Win</div>
                      <div class="fs-5">10</div>
                    </div>
                    <div class="text-center">
                      <span class="fs-4">/</span>
                    </div>
                    <div class="text-center mx-2 text-danger">
                      <div class="fs-4">Losses</div>
                      <div class="fs-5">567</div>
                    </div>
                  </div>
                  <button class="btn btn-primary" @click="goToChangePassword">Change Password</button>
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
                    <h6 class="mb-0"> Name</h6>
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
import { useRouter } from 'vue-router'
import NavHome from './NavHome.vue';
import type Api from '@/utils/Api/Api'
import auth from '../../services/user/services/auth/auth.ts'
import avatar from '/src/assets/avatars/pepe.png'

const api: Api = inject('$api') as Api;
const Auth: auth = new auth(api)

const router = useRouter()

const isEditing = ref(false);
const user = ref({
  username: 'User',
  email: 'email',
  nickname: 'nickname',
  avatarUrl: avatar,
});
const form = ref({
  username: user.value.username,
  email: user.value.email,
  nickname: user.value.nickname,
});

// Avatar Management
//const avatarUrl = ref('https://bootdey.com/img/Content/avatar/avatar7.png'); // URL de ejemplo de avatar
/* const selectedFile = ref<File | null>(null);

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  const file = target.files ? target.files[0] : null;
  if (file) {
    selectedFile.value = file;
    avatarUrl.value = URL.createObjectURL(file); // Mostrar vista previa de la imagen seleccionada
  }
} */

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
  } catch (error: any) {
    window.alert('An error occurred while submitting the form')
    console.error('An error occurred while submitting the form:', error)
  }
}

async function fetchUserData() {
  try {
    const response = await Auth.whoami();
    user.value = {
      username: response.username,
      avatarUrl: response.avatar ? response.avatar : avatar,
    };
    user.value.avatarUrl = '/src/assets/' + user.value.avatarUrl;
    // console.log(user.value.avatarUrl )

    // Check if avatarUrl is set to the default '/src/assets/avatars/pepe.png'
    if (user.value.avatarUrl === '/src/assets/avatars/pepe.png') {
      // Use the default local avatar
      console.log("Using default avatar");
    } else {
      // Retrieve avatar from the backend
      await fetchUserAvatar();   
    }
  } catch (error: any) {
    console.error('Error fetching user data:', error.message);
  }
}

async function fetchUserAvatar() {
  try {
    const response = await api.get('auth/get-avatar');
    if (response.status === 200) {
      const avatarBase64 = response.avatar_base64;
      user.value.avatarUrl = `data:image/jpeg;base64,${avatarBase64}`; // Set the Base64 image as the src
    } else {
      console.error('Failed to fetch avatar:', response.data);
    }
  } catch (error) {
    console.error('Error fetching user avatar:', error.message);
  }
}

onMounted(async () => {
  await fetchUserData();
});

const goToChangeAvatar = () => {
  router.push('/change-avatar')
}

const goToChangePassword = () => {
  router.push('/change-password')
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
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .1), 0 1px 2px 0 rgba(0, 0, 0, .06);
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