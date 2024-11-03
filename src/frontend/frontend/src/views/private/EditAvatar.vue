<template>
  <NavHome></NavHome>

  <div class="container">
    <div class="row d-flex justify-content-center my-5">
      <div class="col-md-6">
        <div class="data-card p-4">
          <div class="text-center">
            <h3 class="mb-4 data-card-title">Upload Avatar</h3>

            <!-- Previsualización de la imagen seleccionada -->
            <img :src="avatarPreview" alt="Avatar Preview" class="mb-4" width="50%" />
            <div class="d-flex justify-content-center flex-column">
              <!-- Input de archivo para seleccionar la imagen -->
              <div class="custom-file-upload align-items-strech">
                <label for="file-input" class="custom-file-label">Upload Avatar</label>
                <input
                  id="file-input"
                  type="file"
                  @change="onFileChange"
                  accept="image/*"
                  class="file-input"
                />
                <span v-if="fileName" class="file-name">{{ fileName }}</span>
              </div>

              <!-- Botón para guardar la imagen subida o cancelar la accion -->
              <div class="d-flex justify-content-center mt-2">
                <button class="btn border-button" @click="uploadAvatar">Save Avatar</button>
                <button class="btn border-button" @click="cancelUpload">Cancel</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/* ----- IMPORTS ----- */

import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import NavHome from './NavHome.vue'

/* ----- VARIABLES ----- */

const api = inject('$api') as any
const router = useRouter()
const avatarPreview = ref('')
const selectedFile = ref<File | null>(null)
const fileName = ref('Introduce tu imagen aqui')

/* ----- PREVISUALIZACION DE LA IMAGEN SELECCIONADA ----- */

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files ? target.files[0] : null
  if (file) {
    fileName.value = file.name
    selectedFile.value = file
    avatarPreview.value = URL.createObjectURL(file) // Previsualización de la imagen seleccionada
  }
}

/* ----- UPLOAD AVATAR ----- */

const uploadAvatar = async () => {
  if (selectedFile.value) {
    const formData = new FormData()
    formData.append('image', selectedFile.value)

    try {
      const response = await api.post('auth/update-avatar', formData)
      if (response.status === 200) {
        router.push('/profile')
      }
    } catch (error: any) {
      console.error('Error uploading avatar:', error)
      alert('An error occurred while uploading the avatar.')
    }
  } else {
    alert('Please select a file before uploading.')
  }
}

/* ----- CANCELAR LA SUBIDA ----- */

const cancelUpload = () => {
  router.push('/profile')
}

/* ----- FETCH AVATAR ----- */

async function fetchUserAvatar() {
  try {
    const response = await api.get('auth/get-avatar')
    if (response.status === 200) {
      const avatarBase64 = response.avatar_base64
      avatarPreview.value = `data:image/jpeg;base64,${avatarBase64}` // Set the Base64 image as the src
    } else {
      console.error('Failed to fetch avatar:', response.data)
    }
  } catch (error: any) {
    console.error('Error fetching user avatar:', error.message)
  }
}

onMounted(async () => {
  await fetchUserAvatar()
})
</script>

<style scoped>
.file-input {
  opacity: 0; /* Oculta el input */
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.custom-file-upload {
  position: relative;
  display: inline-block;
}

.custom-file-label {
  display: inline-block;
  background-color: rgb(206, 29, 82);
  color: #ebd2ff;
  font-family: 'NunitoBlack';
  padding: 11px 15px;
  border-radius: 5px 0 0 5px;
  margin: 0px;
  cursor: pointer;
}

.file-name {
  display: inline-block;
  background-color: transparent;
  color: #ebd2ff;
  font-family: 'Nunito';
  padding: 10px 15px;
  border-radius: 0 5px 5px 0;
  margin: 0px;
  font-size: 0.9em;
  border: 2px solid rgb(206, 29, 82);
}
</style>
