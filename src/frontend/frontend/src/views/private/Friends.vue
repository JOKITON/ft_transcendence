<template>
  <div class="pruebas">
    <NavHome />
  </div>
  <section class="info-section row flex-row-nowrap">
    <div class="info-card d-flex flex-column justify-content-center col-md-6 col-sm-12">
      <h2 class="pt-2">Friends List</h2>
      <div class="card-content">
        <ul class="list-group friends-list">
          <li v-if="friends.length === 0" class="list-group-item text-center">
            No friends available.
          </li>
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
              <span v-if="friend.is_blocked_by_user" class="text-danger">(Bloqueado)</span>
              <span v-if="friend.is_blocked_by_friend" class="text-warning">(Te ha bloqueado)</span>
            </span>
            <div class="btn-group">
              <button class="btn btn-outline-primary btn-sm" @click="handleSendMessage(friend)">
                📩
              </button>
              <button
                v-if="friend.is_blocked_by_user"
                class="btn btn-outline-warning btn-sm"
                @click="unblockUser(friend.username)"
              >
                🔓
              </button>
              <button
                v-else
                class="btn btn-outline-danger btn-sm"
                @click="blockUser(friend.username)"
              >
                🔒
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Tarjeta de Solicitudes de Amistad -->
    <div class="info-card d-flex flex-column justify-content-center col-md-6 col-sm-12">
      <h2 class="pt-2">Friend Requests</h2>
      <div class="card-content">
        <ul class="list-group">
          <li
            v-for="request in friendRequests"
            :key="request.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <span>{{ request.friend.username }}</span>
            <div class="btn-group">
              <button
                class="btn btn-outline-success btn-sm"
                @click="acceptFriendRequest(request.id)"
              >
                ✔️
              </button>
              <button
                class="btn btn-outline-danger btn-sm"
                @click="declineFriendRequest(request.id)"
              >
                ❌
              </button>
            </div>
          </li>
        </ul>
      </div>
      <!-- Búsqueda de Amigos -->
      <div class="search-friend mt-4">
        <input type="text" class="form-control" placeholder="Find user..." v-model="searchQuery" />
        <button class="btn btn-primary mt-2 w-100" @click="sendFriendRequest">
          Enviar Solicitud
        </button>
      </div>
      <div v-if="feedbackMessage" class="alert mt-2" :class="feedbackClass">
        {{ feedbackMessage }}
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// Define las referencias para amigos y solicitudes de amistad


import { ref,onMounted, inject } from 'vue';
import NavHome from './NavHome.vue';
// @ts-ignore
import { eventBus } from './eventbus.js';

// Inyecta el cliente API
const api = inject('$api') as any

const friends = ref<Friend[]>([])
const friendRequests = ref<FriendRequest[]>([])
const searchQuery = ref('')
const feedbackMessage = ref('')
const feedbackClass = ref('')

const handleSendMessage = (friend: Friend) => {
  console.log('Sending message to:', friend)
  eventBus.emit('messageSent', { friend: friend })
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
      api.get('friendship/friends'),
      api.get('auth/whoami')
    ])

    // Asigna el estado correctamente, incluyendo los nuevos campos de bloqueo
    friends.value = (fetchFriendsResponse.friends || []).map((friend) => ({
      ...friend,
      isOnline: friend.isOnline === 'True' // Convertir a booleano
    }))
    form.value = { ...userResponse.data }

    // Fetch friend requests as part of onMounted
    await fetchFriendRequests()
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})

const fetchFriendRequests = async () => {
  try {
    const response = await api.get('friendship/pendingReq')
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
    const myresponse = await api.post('friendship/add', { friend: searchQuery.value })
    console.log('response', myresponse)
    if (myresponse.status === 201) {
      feedbackMessage.value = `Solicitud de amistad enviada a ${searchQuery.value}`
      feedbackClass.value = 'alert-success'
      searchQuery.value = ''
    } else {
      feedbackMessage.value = `Error al enviar solicitud de amistad`
      feedbackClass.value = 'alert-danger'
    }
  } catch (error: any) {
    feedbackMessage.value = `Error al enviar solicitud de amistad: ${error.message}`
    feedbackClass.value = 'alert-danger'
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
}
</script>

<style scoped>
.info-section {
  display: flex;
  justify-content: space-between;
  padding: 40px 20px;
  border-top: solid 2px #ff3974;
  box-shadow: 0px -10px 5px rgba(249, 36, 100, 1);
  overflow-x: auto;
  white-space: nowrap;
}

.info-card {
  background-color: rgba(19, 14, 43, 1);
  color: #ebd2ff;
  text-align: center;
  padding: 1.3em;
  border-radius: 10px;
  margin: 0.8em;
  font-family: Titulo, sans-serif;
  box-shadow: -4px 4px 10px rgba(249, 36, 100, 0.8);
  min-width: 400px;
  flex: 0 0 45%;
}

.card-content {
  max-height: 200px;
  overflow-y: auto;
  margin-top: 10px;
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
}

.search-friend {
  list-style: none;
  padding: 0;
}

.btn-group button {
  font-size: 14px;
  margin: 0 2px;
}

.alert-success {
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.alert-danger {
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

.search-friend input {
  border-radius: 0.25rem;
}
</style>
