<template>
  <div class="pruebas">
    <NavHome></NavHome>
  </div>
  <div class="container">
    <div class="row gutters-sm my-3">
      <div class="col-md-4 d-flex align-items-stretch">
        <div class="user-card w-100 m-3 d-flex justify-content-center">
          <div class="d-flex flex-column justify-content-center align-items-center text-center">
            <h2 class="user-name pb-3 px-3">{{ userData.username }}</h2>
            <img :src="userData.avatar" alt="User Avatar" class="rounded-circle py-3" width="50%">
            <p class="user-alias py-3">{{ userData.nickname }}</p>

            <!-- BOTONES PARA EDITAR LA INFORMACION O EL AVATAR -->
            <div>
              <!-- Mostrar diferentes botones según el estado de la amistad -->
              <button
                v-if="!userData.isFriend && !userData.friendRequestSent"
                class="btn background-button mt-3 mx-2"
                @click="sendFriendRequest"
              >
                Add Friend
              </button>

              <button
                v-if="userData.friendRequestSent && !userData.isFriend"
                class="btn background-button mt-3 mx-2"
                disabled
              >
                Friend Request Sent
              </button>

              <button
                v-if="userData.isFriend"
                class="btn background-button mt-3 mx-2"
                disabled
              >
                Already Friends
              </button>

              <button class="btn border-button mt-3 mx-2" @click="handleSendMessage(userData)">
                Message
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-8 d-flex">
          <Stats v-if="userLoaded" :userId="userData.id"></Stats>
      </div>
    </div>
    <FriendList v-if="userLoaded" :userId="userData.id"></FriendList>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, inject, watch } from 'vue';
import { useRoute } from 'vue-router';
import NavHome from './NavHome.vue';
import Stats from './Stats.vue';
import FriendList from './FriendList.vue';
import { eventBus } from './eventbus.js';

// Tipos e interfaces
interface Friend {
  id: number;
  username: string;
  avatar: string;
  isOnline?: boolean;
  is_blocked_by_user: boolean;
  is_blocked_by_friend: boolean;
}

const api = inject('$api') as Api;
const route = useRoute();

// Variables reactivas
const userId = ref<number | null>(null);
const errorMessage = ref<string | null>(null);
const friends = ref<Friend[]>([]);
const userData = ref({
  id: '',
  username: '',
  nickname: '',
  email: '',
  avatar: '',
  isFriend: false,
  friendRequestSent: false
});
const userLoaded = ref(false);

// Función para enviar mensaje
const handleSendMessage = (friend: Friend) => {
  console.log('Sending message to:', friend);
  eventBus.emit('messageSent', { friend });
};

// Función para enviar solicitud de amistad
const sendFriendRequest = async () => {
  try {
    console.log('Sending friend request to:', userData.value.username);
    await api.post('friendship/add', { friend: userData.value.username });
    console.log(`Friend request sent to ${userData.value.username}`);
    userData.value.friendRequestSent = true;
  } catch (error) {
    console.error('Error sending friend request', error);
  }
};

// Función para comprobar si es amigo
const checkIfFriend = (friends: Friend[], userId: number) => {
  console.log('Checking if user is friend:', friends, userId);
  return friends.some(friend => friend.id === userId);
};

// Función para cargar los datos del usuario
const fetchUserData = async (id: number) => {
  try {
    const response = await api.get(`auth/search-user-id/${id}/`);
    userData.value = {
      id: response.user_data.id,
      username: response.user_data.username,
      nickname: response.user_data.nickname,
      email: response.user_data.email,
      avatar: response.user_data.avatar,
      isFriend: checkIfFriend(friends.value, response.user_data.id),
      friendRequestSent: false
    };
    userLoaded.value = true;
  } catch (error) {
    console.error('Error fetching user data:', error);
    errorMessage.value = 'Error al cargar los datos del usuario';
  }
};

// Función para cargar el avatar del usuario
const fetchUserAvatar = async (id: number) => {
  try {
    const response = await api.get(`auth/get-avatar-id/${id}/`);
    if (response.status === 200) {
      const avatarBase64 = response.avatar_base64;
      userData.value.avatar = `data:image/jpeg;base64,${avatarBase64}`;
    }
  } catch (error : any) {
    console.error('Error fetching user avatar:', error.message);
  }
};

// Observar cambios en los parámetros de la ruta
watch(() => route.params.id, (newId: string) => {
  userId.value = parseInt(newId, 10)
  if (userId.value) {
    fetchUserData(userId.value);
    fetchUserAvatar(userId.value);
  }
});

// Cargar amigos y datos del usuario cuando se monta el componente
onMounted(async () => {
  try {
    userId.value = parseInt(route.params.id, 10);
    if (userId.value) {
      // Cargar lista de amigos
      const response = await api.get<{ friends: Friend[] }>(`friendship/friends`);
      friends.value = (response.friends || []).map(friend => ({
        ...friend,
        isOnline: friend.isOnline === 'True'
      }));

      // Cargar los datos del usuario
      await fetchUserData(userId.value);
      await fetchUserAvatar(userId.value);
    }
  } catch (error) {
    console.error('Error al cargar los amigos o datos del usuario:', error);
  }
});
</script>

  
  
<style scoped>

.user-alias {
  font-family: NunitoBlack !important;
  color:#ebd2ff;
  margin-bottom: 0px;
  font-size: 1.2em;
}
  
.user-name {
  font-family: Titulo !important;
  color:#ebd2ff;
  margin-bottom: 0px;
}

.pruebas {
  position: relative;
  z-index: 100;
}
</style>