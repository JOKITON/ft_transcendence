<template>
  <NavHome></NavHome>
  
  <div class="container">
    <div class="row justify-content-center">

      <!-- Formulario para editar los datos del usuario -->
      <div class="col-md-6">
        <div class="data-card p-4 my-5">
          <h4 class="mb-4 text-center card-title">Update User Data</h4>
          <form @submit.prevent="updateUserData">

            <!-- Cambiar nombre -->
            <div class="mb-3">
              <label for="newName" class="data-label">New Name</label>
              <input
                type="username" 
                id="username" 
                v-model="formUserData.newUsername" 
                class="data-control data-placeholder" 
                placeholder="Enter your new name"
                required/>
            </div>
    
            <!-- Cambiar nickname -->
            <div class="mb-3">
              <label for="newNickname" class="data-label">New Nickname</label>
              <input 
                type="nickname" 
                id="nickname" 
                v-model="formUserData.newNickname" 
                class="data-control data-placeholder" 
                placeholder="Enter your new nickname"
                required/>
            </div>
    
            <!-- Cambiar email -->
            <div class="mb-4">
              <label for="newMail" class="data-label">New mail</label>
              <input 
                type="Email" 
                id="email" 
                v-model="formUserData.newEmail" 
                class="data-control data-placeholder" 
                placeholder="Enter your new email"
                required/> 
            </div>

            <!-- Botón para guardar la informacion -->
            <div class="d-flex justify-content-center">
              <button type="submit" class="btn data-button">Update User Data</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Formulario para editar la contraseña del usuario -->
      <div class="col-md-6">
        <div class="data-card p-4 my-5">
          <h4 class="mb-4 text-center card-title">Update Password</h4>
          <form @submit.prevent="updatePassword">
            
            <!-- Current Password -->
            <div class="mb-3">
              <label for="currentPassword" class="data-label">Current Password</label>
              <input
                type="password" 
                id="currentPassword" 
                v-model="formPasswd.currentPassword" 
                class="data-control data-placeholder" 
                placeholder="Enter your current password" 
                required>
            </div>

            <!-- New Password -->
            <div class="mb-3">
              <label for="newPassword" class="data-label">New Password</label>
              <input 
                type="password" 
                id="newPassword" 
                v-model="formPasswd.newPassword" 
                class="data-control data-placeholder" 
                placeholder="Enter your new password" 
                required
              />
            </div>

            <!-- Confirm New Password -->
            <div class="mb-4">
              <label for="confirmPassword" class="data-label">Confirm New Password</label>
              <input 
                type="password" 
                id="confirmPassword" 
                v-model="formPasswd.confirmPassword" 
                class="data-control data-placeholder" 
                placeholder="Confirm your new password" 
                required
                /> 
            </div>

            <!-- Update Button -->
            <div class="d-flex justify-content-center">
              <button type="submit" class="btn data-button">Update Password</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">

/* ----- IMPORTS ----- */

import { ref, inject, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import type { passwdRequest, passwdResponse} from '@/models/user/passwdRequest'
import type { userDataRequest, userDataResponse } from '@/models/user/userDataRequest';

import auth from '../../services/user/services/auth/auth.js'

import NavHome from './NavHome.vue';


/* ----- VARIABLES ----- */

const api = inject('$api') as any;
const Auth: auth = new auth(api)
const router = useRouter()

const formPasswd = ref<passwdRequest>({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const formUserData = ref<userDataRequest>({
  newUsername: '',
  newNickname: '',
  newEmail: ''
});

/* To restore the original user data values */
const originalUserData = ref<userDataRequest>({
  newUsername: '',
  newNickname: '',
  newEmail: ''
});


/* ----- HANDLE UPDATES ----- */

const updatePassword: () => Promise<void> = async () => {
  try {
    const response = await api.post("auth/change-password",formPasswd.value)
    if (response.status == 400) {
      window.alert('An error occurred while submitting the form')
      resetPasswdForm()
    } else if (response.status == 200) {
      router.push('/profile')
    }
  } catch (error: any) {
    window.alert('An error occurred while submitting the form')
    console.error('An error occurred while submitting the form:', error)
    resetPasswdForm()
  }
};

const updateUserData: () => Promise<void> = async() => {
  try {
    const response = await api.post("auth/update-profile",formUserData.value)
    if (response.status == 200) {
      router.push('/profile')
    } else {
      window.alert('Los datos introducidos son de otro usuario.')
      resetUserDataForm()
    }
  } catch (error: any) {
    window.alert('An error occurred while submitting the form')
    console.error('An error occurred while submitting the form:', error)
    resetUserDataForm()
  }
}


/* ----- RESET FORMS ----- */

const resetPasswdForm = () => {
  formPasswd.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  };
};

const resetUserDataForm = () => {
  formUserData.value = { ...originalUserData.value };
};


/* ----- FETCHING DATA ----- */

async function fetchUserData() {
  try {
    const response : any = await Auth.whoami();
    console.log(response)
    formUserData.value = {
      newUsername: response.username,
      newEmail: response.email,
      newNickname: response.nickname,
    };
    originalUserData.value = { ...formUserData.value };
  } catch (error: any) {
    console.error('Error fetching user data:', error.message);
  }
}

onMounted(async () => {
  await fetchUserData();
});

</script>

<style scoped>

.card-title {
  color: #f92464;
  font-family: 'Titulo';
}

</style>
