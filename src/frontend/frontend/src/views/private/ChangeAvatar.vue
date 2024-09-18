<template>
    <NavHome></NavHome>
  
    <div class="container">
      <div class="main-body d-flex justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <h4 class="mb-4">Upload New Avatar</h4>
  
              <!-- Previsualización de la imagen seleccionada -->
              <img :src="avatarPreview" alt="Avatar Preview" class="rounded-circle mb-4" width="250">
  
              <!-- Input de archivo para seleccionar la imagen -->
              <input type="file" @change="onFileChange" class="form-control mb-3" accept="image/*" />
  
              <!-- Botón para guardar la imagen subida -->
              <button class="btn btn-primary" @click="uploadAvatar">Save Avatar</button>
              <button class="btn btn-secondary ms-2" @click="cancelUpload">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, inject } from 'vue';
  import { useRouter } from 'vue-router';
  import avatar from './pepe.png';
  
  const api: Api = inject('$api') as Api;
  const router = useRouter();
  // Imagen de previsualización por defecto o avatar actual del usuario
  const avatarPreview = ref(avatar); 
  const selectedFile = ref<File | null>(null);
  
  // Manejo del cambio de archivo seleccionado
  const onFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const file = target.files ? target.files[0] : null;
    if (file) {
      selectedFile.value = file;  
      avatarPreview.value = URL.createObjectURL(file); // Previsualización de la imagen seleccionada
    }
  }
  
  // Subir el avatar al servidor
/*   const uploadAvatar = async () => {
    if (selectedFile.value) {
      const formData = new FormData();
      formData.append('avatar', selectedFile.value);
  
      try {
        const response = await api.post('change-avatar', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        if (response.status === 200) {
          alert('Avatar updated successfully!');
          router.push('/profile'); // Redirigir al perfil del usuario tras subir avatar
        }
      } catch (error) {
        console.error('Error uploading avatar:', error);
        alert('An error occurred while uploading the avatar.');
      }
    } else {
      alert('Please select a file before uploading.');
    }
  } */
  
  // Cancelar la subida y redirigir al perfil del usuario
  const cancelUpload = () => {
    router.push('/profile');
  }
  
  // Cargar el avatar actual del usuario al montar el componente (opcional)
/*   async function fetchAvatar() {
    try {
      const response = await api.get('get-avatar');
      avatarPreview.value = response.avatarUrl || avatarPreview.value; // Usar el avatar actual o mantener la imagen por defecto
    } catch (error: any) {
      console.error('Error fetching avatar:', error.message);
    }
  }
  
  onMounted(async () => {
    await fetchAvatar();
  }); */
  </script>
  
  <style scoped>
  .main-body {
    padding: 30px;
  }
  .card {
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  .card-body {
    padding: 20px;
  }
  </style>