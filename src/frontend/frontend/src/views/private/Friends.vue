<template>
  <div class="pruebas">
    <NavHome ></NavHome>
  </div>
  <div class="row gutters-sm">
    <div class="col-sm-6 mb-3">
      <div class="card h-100 card-scrollable">
        <div class="card-body">
          <h6 class="d-flex align-items-center mb-3">Friends List</h6>
          <ul class="list-group friends-list">
            <li
              v-for="friend in friends"
              :key="friend.id"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <span>
                <span
                  :class="['status-indicator', friend.isOnline ? 'bg-success' : 'bg-danger']"
                ></span>
                {{ friend.username }}
                <span v-if="friend.is_blocked_by_user" class="text-danger">(Bloqueado por ti)</span>
                <span v-if="friend.is_blocked_by_friend" class="text-warning"
                  >(Te ha bloqueado)</span
                >
              </span>
              <div class="btn-group">
                <button class="btn btn-primary btn-sm" @click="handleSendMessage(friend)" :disabled="friend.is_blocked_by_friend">Mensaje</button>

                <button v-if="friend.is_blocked_by_user" class="btn btn-warning btn-sm" @click="unblockUser(friend.username)">
                  Desbloquear
                </button>
                <button v-else class="btn btn-danger btn-sm" @click="blockUser(friend.username)" :disabled="friend.is_blocked_by_friend">
                  Bloquear
                </button>
                <button
                  class="btn btn-success btn-sm"
                  @click="inviteUser(friend.username)"
                  :disabled="friend.is_blocked_by_friend"
                >
                  Invitar
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- Solicitudes de amistad -->
    <div class="col-sm-6 mb-3">
      <div class="user-card  h-100 card-scrollable">
        <div class="card-body card-body2">
          <h6 class="d-flex align-items-center mb-3">Friend Requests</h6>
          <div class="d-flex flex-column">
            <ul class="list-group">
              <li
                v-for="request in friendRequests"
                :key="request.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <span>
                  <span class="status-indicator bg-success"></span>
                  {{ request.friend.username }}
                </span>
                <div class="btn-group">
                  <button class="btn btn-success btn-sm" @click="acceptFriendRequest(request.id)">
                    Aceptar
                  </button>
                  <button class="btn btn-danger btn-sm" @click="declineFriendRequest(request.id)">
                    Rechazar
                  </button>
                </div>
              </li>
            </ul>
          </div>
          <div class="search-friend mt-4">
            <input
              type="text"
              class="form-control"
              placeholder="Buscar usuario..."
              v-model="searchQuery"
            />
            <button class="btn btn-primary mt-2 w-100" @click="sendFriendRequest">Enviar</button>
          </div>
          <div v-if="feedbackMessage" class="alert" :class="feedbackClass">{{ feedbackMessage }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

// Define las referencias para amigos y solicitudes de amistad


import { ref,onMounted, inject } from 'vue';
import { defineEmits } from 'vue';
import NavHome from './NavHome.vue';
import { eventBus } from './eventbus.js';
import DesplegableChat from './DesplegableChat.vue';

// Inyecta el cliente API
const api = inject('$api') as any;

const friends = ref<Friend[]>([])
const friendRequests = ref<FriendRequest[]>([])
const searchQuery = ref('');
const feedbackMessage = ref('');
const feedbackClass = ref('');

const handleSendMessage = (friend) => {
  console.log('Sending message to:', friend);
  eventBus.emit('messageSent', { friend: friend });
}
interface Friend {
  id: number
  username: string
  avatar: string
  isOnline?: boolean
  is_blocked_by_user: boolean
  is_blocked_by_friend: boolean
}

interface FriendRequest {
  id: number
  friend: {
    username: string
    email: string
  }
}

// Define la estructura para la respuesta de la API de solicitudes de amistad
interface FriendRequestsResponse {
  pending_requests: FriendRequest[]
}

const form = ref({
  username: '',
  email: '',
  nickname: ''
})

onMounted(async () => {
  try {
    // Fetch friends and user data
    const [fetchFriendsResponse, userResponse] = await Promise.all([
      api.get<Friend[]>('friendship/friends'),
      api.get<{ username: string; email: string; nickname: string }>('auth/whoami')
    ])

    // Asigna el estado correctamente, incluyendo los nuevos campos de bloqueo
    friends.value = (fetchFriendsResponse.friends || []).map(friend => ({
      ...friend,
      isOnline: friend.isOnline === 'True'  // Convertir a booleano
    }));
    form.value = { ...userResponse.data };

    // Fetch friend requests as part of onMounted
    await fetchFriendRequests()
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})

const fetchFriendRequests = async () => {
  try {
    const response = await api.get<FriendRequestsResponse>('friendship/pendingReq')
    friendRequests.value = response.pending_requests || []
  } catch (error: any) {
    console.error('Error fetching friend requests:', error.message)
  }
}

const blockUser = async (username: string) => {
  try {
    await api.post('friendship/blockFriend', { friend_username: username })
    console.log(`User ${username} blocked successfully`)
    friends.value = friends.value.map((friend) =>
      friend.username === username ? { ...friend, is_blocked_by_user: true } : friend
    )
  } catch (error) {
    console.error('Error blocking user', error)
  }
}

const unblockUser = async (username: string) => {
  try {
    await api.post('friendship/unblockFriend', { friend_username: username })
    console.log(`User ${username} unblocked successfully`)
    friends.value = friends.value.map((friend) =>
      friend.username === username ? { ...friend, is_blocked_by_user: false } : friend
    )
  } catch (error) {
    console.error('Error unblocking user', error)
  }
}


const inviteUser = async (username: string) => {
  try {
    await api.post('/invite-user/', { friend: username })
    console.log(`Invitation sent to ${username}`)
  } catch (error) {
    console.error('Error sending invitation', error)
  }
}

const sendFriendRequest = async () => {
  try {
    const myresponse = await api.post('friendship/add', { friend: searchQuery.value });
    console.log('response', myresponse);
    if (myresponse.status === 201) {
      feedbackMessage.value = `Solicitud de amistad enviada a ${searchQuery.value}`;
      feedbackClass.value = 'alert-success';
      searchQuery.value = '';
    } else {
      feedbackMessage.value = `Error al enviar solicitud de amistad`;
      feedbackClass.value = 'alert-danger';
    }
  } catch (error) {
    feedbackMessage.value = `Error al enviar solicitud de amistad: ${error.message}`;
    feedbackClass.value = 'alert-danger';
  }
}

const acceptFriendRequest = async (requestId: number) => {
  try {
    await api.post('friendship/acceptFriendReq', { request_id: requestId })
    console.log(`Friend request ${requestId} accepted`)
    await fetchFriendRequests()
  } catch (error) {
    console.error('Error accepting friend request', error)
  }
}

const declineFriendRequest = async (requestId: number) => {
  try {
    await api.post('friendship/rejectFriendReq', { request_id: requestId })
    console.log(`Friend request ${requestId} declined`)
    console.log('nombre de la sala')
    await fetchFriendRequests()
  } catch (error) {
    console.error('Error declining friend request', error)
  }
};

</script>

<style scoped>
.friends-list {
  max-height: 200px;
  overflow-y: auto;
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 5px;
}

.bg-success {
  background-color: green;
}

.bg-danger {
  background-color: red;
}
.pruebas {
  position: relative;
  z-index: 100;
}

.alert-success {
  color: #155724;
  background-color: #d4edda;
  border-color: #c3e6cb;
}
.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

</style>
