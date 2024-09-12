<template>
  <NavHome></NavHome>

  <div class="container">
    <div class="main-body">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h4 class="mb-4 text-center">Update Password</h4>
              <form @submit.prevent="updatePassword">
                <!-- Current Password -->
                <div class="form-group mb-3">
                  <label for="currentPassword">Current Password</label>
                  <input type="password" id="currentPassword" v-model="form.currentPassword" class="form-control" required>
                </div>

                <!-- New Password -->
                <div class="form-group mb-3">
                  <label for="newPassword">New Password</label>
                  <input type="password" id="newPassword" v-model="form.newPassword" class="form-control" required>
                </div>

                <!-- Confirm New Password -->
                <div class="form-group mb-4">
                  <label for="confirmPassword">Confirm New Password</label>
                  <input type="password" id="confirmPassword" v-model="form.confirmPassword" class="form-control" required>
                </div>

                <!-- Update Button -->
                <div class="d-grid gap-2">
                  <button type="submit" class="btn btn-primary">Update Password</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue';
import NavHome from './NavHome.vue';
import { useRouter } from 'vue-router'
import type { passwdRequest, passwdResponse} from '@/models/user/passwdRequest'


const api: Api = inject('$api') as Api;
const router = useRouter()
// Form data
const form = ref<passwdRequest>({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

// Function to handle password update
const updatePassword: () => Promise<void> = async () => {
  try {
    console.log(form.value)
    const response = await api.post<passwdResponse>("change-password",form.value)
    console.log('saved successful ', response)
    if (response.status == 400) {
      window.alert('An error occurred while submitting the form')
      router.push('/profile')
    } else if (response.status == 200) {
      router.push('/pong')
    }
    //window.location.reload();
  } catch (error: any) {
    window.alert('An error occurred while submitting the form')
    console.error('An error occurred while submitting the form:', error)
  }
};
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
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .1), 0 1px 2px 0 rgba(0, 0, 0, .06);
  background-color: #fff;
  border-radius: .25rem;
}

.card-body {
  padding: 20px;
}

h4 {
  color: #333;
}
</style>
