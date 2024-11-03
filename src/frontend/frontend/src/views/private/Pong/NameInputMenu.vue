<template>
  <div class="form-container">
    <div class="form-content">
      <h2 class="title">Play Menu</h2>
      <form @submit.prevent="startGame" class="game-form">
        <div class="d-flex justify-content-center mt-4">
          <!-- Toggle buttons for Online/Offline mode -->
          <button
            type="button"
            class="btn btn-lg mx-2"
            :class="{
              'btn-primary': isOnline === 'Online',
              'btn-outline-primary': isOnline !== 'Online'
            }"
            @click="setGameMode('Online')"
          >
            Online
          </button>
          <button
            type="button"
            class="btn btn-lg mx-2"
            :class="{
              'btn-secondary': isOnline === 'Offline',
              'btn-outline-secondary': isOnline !== 'Offline'
            }"
            @click="setGameMode('Offline')"
          >
            Offline
          </button>
        </div>

        <div v-if="isOnline" class="player-inputs">
          <h3 class="mb-3">Choose Game Mode:</h3>
          <div class="game-mode-options">
            <label v-if="isOnline === 'Offline'" class="game-mode-label">
              <input v-model="gameMode" type="radio" value="AI" required />
              One Player (vs AI)
            </label>
            <label class="game-mode-label">
              <input v-model="gameMode" type="radio" value="2P" required />
              Two Player
            </label>
            <label class="game-mode-label">
              <input v-model="gameMode" type="radio" value="4P" required />
              Tournament (4|8 Player)
            </label>
          </div>
        </div>

        <!-- Player Input Fields -->
        <div v-if="gameMode" class="player-inputs">
          <span v-if="gameMode === 'AI'" class="vs-text">
            {{ userOne.nickname }} VS AI
            <div class="form-check form-switch" style="margin-left: 10px">
              <input
                class="form-check-input"
                type="checkbox"
                v-model="isAudioEnabled"
                id="audioSwitch"
              />
              <label class="form-check-label" for="audioSwitch">Enable Audio</label>
            </div>
          </span>

          <div v-if="gameMode !== 'AI'" class="player-group">
            <div class="player-group">
              <!-- Inside your player group for two-player mode -->
              <div v-if="gameMode === '2P'" class="player-group">
                <span class="player-nickname">{{ userOne.nickname }}</span>
                <span class="vs-text">VS</span>
                <select class="form-select" required>
                  <option value="" disabled>Select Opponent</option>
                  <option v-for="user in orUsers" :key="user.nickname" :value="user.nickname">
                    {{ user.nickname }}
                  </option>
                </select>
              </div>

              <!-- Inside your player group for eight-player mode -->
              <div v-if="gameMode === '4P' && (users.length == 4 || users.length == 8)">
                <div v-for="(user, index) in users" :key="index" class="player-group">
                  <!-- The player that should be in the left side of the column for the Tournament -->
                  <div
                    v-if="index % 2 == 0"
                    class="player-select-wrapper"
                    style="display: flex; align-items: center"
                  >
                    <select class="form-select" required>
                      <option value="" disabled>Select Opponent</option>
                      <option
                        v-for="filteredUser in filteredUsers(index)"
                        :key="filteredUser.nickname"
                        :value="filteredUser.nickname"
                      >
                        {{ filteredUser.nickname }}
                      </option>
                    </select>
                    <span class="vs-text" style="margin-left: 10px">VS</span>
                    <select class="form-select" required>
                      <option value="" disabled>Select Opponent</option>
                      <option
                        v-for="filteredUser in filteredUsers(index + 1)"
                        :key="filteredUser.nickname"
                        :value="filteredUser.nickname"
                      >
                        {{ filteredUser.nickname }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- AI Difficulty Selection for One Player Mode -->
          <div v-if="gameMode === 'AI'" class="ai-difficulty">
            <select v-model="aiDifficulty" class="form-select" required>
              <option value="">Choose difficulty...</option>
              <option value="0.3">Easy</option>
              <option value="0.5">Normal</option>
              <option value="1">Hard</option>
              <option value="1.5">Impossible</option>
            </select>
          </div>
        </div>

        <button
          v-if="
            gameMode &&
            (gameMode === 'AI' ||
              (gameMode === '2P' && users.length >= 2) ||
              (gameMode === '4P' && (users.length == 4 || users.length == 8)))
          "
          type="submit"
          class="btn btn-primary mt-4"
        >
          Start Game
        </button>
      </form>
    </div>
    <div class="trophy-container">
      <img :src="img1" alt="Trophy" class="trophy-image" />
    </div>
    <!-- Leaderboard Section -->
    <div class="leaderboard-container">
      <div class="leaderboard">
        <h6 class="leaderboard-title">Leaderboard</h6>
        <ul class="list-group">
          <li
            v-for="(user) in leaderboard"
            :key="user.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <span class="badge text-dark">
              <span v-if="user.status == 'True'" :class="['status-indicator', 'bg-success']"></span>
              <span
                v-else-if="user.status == 'Offline'"
                :class="['status-indicator', 'bg-danger']"
              ></span>
              <span v-else :class="['status-indicator', 'bg-warning']"></span>
              {{ user.name }}
            </span>
            <span class="badge bg-primary rounded-pill">{{ user.wins }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, inject } from 'vue'
import type Api from '@/utils/Api/Api'
import auth from '@/services/auth/auth'
import img1 from 'assets/avatars/trophy.png';

const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)

const isOnline = ref('') // Keep track of whether Online or Offline is selected
const gameMode = ref('')
const isAudioEnabled = ref(false)
const aiDifficulty = ref(1)

// Sample leaderboard data
const leaderboard = ref<LeaderboardEntry[]>([]) // Initialize the leaderboard as a single array of LeaderboardEntry objects

// Function to print the length of the leaderboard array
function printLeaderboardLength() {
}

onMounted(async () => {
  await fetchNickname()
  await fetchUserList()
  await fetchLeaderboard()
})

interface LeaderboardEntry {
  id: number
  name: string
  wins: number
  status: string
}

interface User {
  id: number
  username: string
  nickname: string
  status: string
}

const users = ref<User[]>([])
const orUsers = ref<User[]>([])
const userOne = ref<User>() // Assuming you want to store the fetched user

// Set the default leaderboard data
const setDefaultLeaderboard = async () => {
  leaderboard.value = [{ id: 0, name: 'No data found', wins: 0, status: 'Offline' }]
}

const fetchLeaderboard = async () => {
  try {
    const response = await api.get('pong/leaderboard')
    if (response.data == 0) {
      setDefaultLeaderboard()
    } else {
      leaderboard.value = (response.data as LeaderboardEntry[]) || [] // Ensure you access the data property

      for (let i = 0; i < users.value.length; i++) {
        for (let j = 0; j < users.value.length; j++) {
          if (leaderboard.value[i].name === users.value[j].nickname) {
            leaderboard.value[i].status = users.value[j].status
          }
        }
      }
    }
  } catch (error: any) {
    console.error(
      'Error fetching leaderboard:',
      error.response ? error.response.data : error.message
    )
  }
}

const fetchUserList = async () => {
  try {
    const response = await api.get<User[]>('friendship/users')
    users.value = response.data || []

    orUsers.value = [...users.value]

    // Add the user from fetchNickname() at the first position
    if (userOne.value) {
      users.value.unshift(userOne.value) // Add the user to the start of the array
    }

  } catch (error: any) {
    console.error('Error fetching users:', error.response ? error.response.data : error.message)
  }
}

async function fetchNickname() {
  try {
    const response = await Auth.whoami()
    userOne.value = {
      id: response.id,
      username: response.username,
      nickname: response.nickname,
      status: 'True'
    }
  } catch (error: any) {
    console.error('Error fetching user data:', error.message)
  }
}

const emit = defineEmits(['startGame'])

// Function to set the game mode (Online/Offline)
const setGameMode = (mode) => {
  isOnline.value = mode
  gameMode.value = '' // Reset game mode when switching between Online/Offline
}

const filteredUsers = (currentIndex) => {
  return users.value.filter(
    (user) =>
      !users.value.some(
        (selectedUser, index) => index !== currentIndex && selectedUser.nickname === user.nickname
      )
  )
}

const startGame = () => {
  const data = {
    gameMode: gameMode.value,
    players: [],
    isAudioEnabled: isAudioEnabled.value,
    aiDifficulty: aiDifficulty.value,
  }

  if (gameMode.value === 'AI') {
    data.players.push({
      player: userOne.value.nickname,
      id: userOne.value.id
    })
    data.aiDifficulty = aiDifficulty.value
  } else if (gameMode.value === '2P') {
    const selectedOpponent = (document.querySelector('.player-group select') as HTMLSelectElement).value
    const opponent = users.value.find((user) => user.nickname === selectedOpponent)
    if (opponent) {
      data.players.push({
        player: userOne.value.nickname,
        id: userOne.value.id
      })
      data.players.push({
        player: opponent.nickname,
        id: opponent.id
      })
    }
  } else if (gameMode.value === '4P') {
    const selects = document.querySelectorAll('.player-select-wrapper select')
    selects.forEach((select) => {
      const selectedNickname = (select as HTMLSelectElement).value
      const selectedUser = users.value.find((user) => user.nickname === selectedNickname)
      if (selectedUser) {
        data.players.push({
          player: selectedUser.nickname,
          id: selectedUser.id
        })
      }
    })
  }

  emit('startGame', data)
}
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-top: solid 2px #ff3974;
  box-shadow: 0px -10px 5px rgba(249, 36, 100, 1);
}

.form-content {
  background-color: rgba(19, 14, 43, 1);
  color: #ebd2ff;
  border-radius: 10px;
  padding: 2em;
  box-shadow: -4px 4px 10px rgba(249, 36, 100, 0.8);
  width: 100%;
  max-width: 600px; /* Ajusta el ancho máximo */
}

.title {
  text-align: center;
  font-family: Titulo, sans-serif;
  margin-bottom: 20px;
}

.player-inputs {
  margin-top: 20px;
}

.game-mode-label {
  margin-right: 20px;
}

.ai-difficulty {
  margin-top: 20px;
}

.trophy-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.trophy-image {
  width: 100px; /* Ajusta el tamaño de la imagen del trofeo */
}

.leaderboard-container {
  margin-top: 30px;
  width: 100%; /* Ocupa todo el ancho disponible */
  max-width: 400px; /* Ajusta el ancho máximo para que sea más estrecho */
  background-color: rgba(19, 14, 43, 1); /* Fondo del leaderboard */
  border-radius: 10px;
  padding: 1.5em; /* Espaciado interno */
  box-shadow: -4px 4px 10px rgba(249, 36, 100, 0.8); /* Sombra */
  margin-left: auto; /* Centrar el contenedor */
  margin-right: auto; /* Centrar el contenedor */
}

.leaderboard-title {
  text-align: center;
  margin-bottom: 20px;
  font-family: Titulo, sans-serif;
  color: #ff3974;
  font-size: 1.5em;
}

.list-group {
  list-style: none;
  padding: 0;
}

.list-group-item {
  background-color: rgba(30, 30, 30, 0.8); /* Fondo de los elementos de la lista */
  color: #ebd2ff; /* Color del texto */
  border-radius: 8px; /* Esquinas redondeadas */
  margin: 5px 0; /* Espaciado entre los elementos */
  display: flex;
  justify-content: space-between;
  align-items: center; /* Alinear contenido */
  padding: 10px 15px; /* Espaciado interno */
  transition: background-color 0.3s; /* Transición suave */
}

.list-group-item:hover {
  background-color: rgba(249, 36, 100, 0.9); /* Cambio de color al pasar el mouse */
}

.badge {
  background-color: #ff3974; /* Color de las insignias */
  color: #fff; /* Color del texto de las insignias */
  padding: 5px 10px; /* Espaciado interno */
  border-radius: 12px; /* Esquinas redondeadas para las insignias */
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
}

.btn-primary {
  background-color: #ff3974;
  border: none;
}

.btn-outline-primary {
  border-color: #ff3974;
  color: #ff3974;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-outline-secondary {
  border-color: #6c757d;
  color: #6c757d;
}
</style>
