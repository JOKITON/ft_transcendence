<template>
  <div class="my-5">
    <h2 class="text-center titulo">Amigos</h2>
    <div v-for="friend in friends" :key="friend.id" class="row d-flex justify-content-center">
      <div class="friend-box d-flex m-5">
        <div
          class="col-md-1 friend-item d-flex flex-column align-items-center"
          @click="goToUserProfile(friend.id)"
        >
          <img :src="friend.avatar" alt="User Avatar" class="py-3" width="50%" />
          <p class="friend-name">{{ friend.username }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.titulo {
  color: #ebd2ff !important;
  font-family: 'Titulo' !important;
  padding: 0.5em;
  background-color: rgba(19, 14, 43, 0.95);
  box-shadow: -4px 4px 10px rgba(249, 36, 100, 255);
}

.friend-box {
  height: 125px !important;
  width: 125px !important;
  background: linear-gradient(45deg, #ad2bf1, #ff3974) !important;
  box-shadow: -2px 2px 5px #ad2bf1;
  padding: 0px !important;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  transition: 0.2s ease-out;
}

.friend-box:hover {
  transform: scale(1.2);
  opacity: 1;
}

.friend-item {
  height: 120px;
  width: 120px;
  font-size: 20px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(19, 14, 43, 0.9);
  transition: 0.2s ease-out;
}

.friend-name {
  font-family: 'NunitoBlack';
  color: #ebd2ff;
}
</style>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import avatar from '../../assets/avatars/pepe.png'

const api = inject('$api') as Api
const router = useRouter()

const friends = ref<Friend[]>([])

const props = defineProps({
  userId: {
    type: Number,
    required: true
  }
})

interface Friend {
  id: number
  username: string
  avatar: string
  isOnline?: boolean
  is_blocked_by_user: boolean
  is_blocked_by_friend: boolean
}

const fetchUserAvatar = async (friend: Friend) => {
  try {
    const response = await api.get(`auth/get-avatar-id/${friend.id}/`)
    if (response.status === 200) {
      const avatarBase64 = response.avatar_base64
      friend.avatar = `data:image/jpeg;base64,${avatarBase64}`
    } else {
      console.error('Failed to fetch avatar:', response.data)
    }
  } catch (error: any) {
    console.error('Error fetching user avatar:', error.message)
  }
}

const goToUserProfile = (userId: number) => {
  router.push(`/user-profile/${userId}`)
}

onMounted(async () => {
  try {
    // Fetch friends and user data
    const fetchFriendsResponse = await api.get<Friend[]>(`friendship/friends-id/${props.userId}/`)
    friends.value = fetchFriendsResponse.friends || []
    friends.value.forEach((friend) => {
      fetchUserAvatar(friend)
    })
  } catch (error: any) {
    console.error('Error fetching data:', error)
  }
})
</script>
