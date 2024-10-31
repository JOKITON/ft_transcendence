<template>
  <div class="form-container">
    <div class="form-content">
      <h2 class="title">Play Menu</h2>
      <form @submit.prevent="startGame" class="game-form">
        <div class="d-flex justify-content-center mt-4 mode-toggle">
          <h5 class="OnlineTitle">Select Option:</h5>
          <!-- Toggle buttons for Online/Offline mode -->
          <button
            type="button"
            class="btn toggle-btn mx-2"
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
            class="btn toggle-btn mx-2"
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
              <input v-model="gameMode" type="radio" value="onePlayer" required />
              One Player (vs AI)
            </label>
            <label class="game-mode-label">
              <input v-model="gameMode" type="radio" value="twoPlayer" required />
              Two Player
            </label>
            <label class="game-mode-label">
              <input v-model="gameMode" type="radio" value="eightPlayer" required />
              Tournament (8 Player)
            </label>
          </div>
        </div>

        <!-- Player Input Fields -->
        <div v-if="gameMode" class="player-inputs">
          <div v-for="(player, index) in filteredPlayers" :key="index" class="player-group">
            <input
              v-model="players[index].name1"
              :placeholder="'Enter Player ' + (index * 2 + 1) + ' Name'"
              class="form-control player-input"
              required
            />
            <span v-if="gameMode !== 'onePlayer'" class="vs-text">VS</span>
            <input
              v-if="gameMode !== 'onePlayer'"
              v-model="players[index].name2"
              :placeholder="'Enter Player ' + (index * 2 + 2) + ' Name'"
              class="form-control player-input"
              required
            />
          </div>

          <!-- AI Difficulty Selection for One Player Mode -->
          <div v-if="gameMode === 'onePlayer'" class="ai-difficulty">
            <select v-model="aiDifficulty" class="form-select" required>
              <option value="">Choose difficulty...</option>
              <option value="0.3">Easy</option>
              <option value="0.5">Normal</option>
              <option value="1">Hard</option>
              <option value="1.5">Impossible</option>
            </select>
          </div>
        </div>

        <button v-if="gameMode" type="submit" class="btn btn-primary mt-4 submit-btn">
          Start Game
        </button>
      </form>
    </div>

    <!-- Trophy Image -->
    <div class="trophy-container">
      <img :src="img1" alt="Trophy" class="trophy-image" />
    </div>

    <!-- Leaderboard Section -->
    <div class="leaderboard-container">
      <div class="leaderboard">
        <h6 class="leaderboard-title">Leaderboard</h6>
        <ul class="list-group leaderboard-list">
          <li
            v-for="user in leaderboard"
            :key="user.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <span>
              <span :class="['status-indicator', user.status]"></span>
              {{ user.name }}
            </span>
            <span class="badge bg-primary rounded-pill">{{ user.score }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import img1 from '../../../assets/avatars/trofeo.png' // Import the trophy image

const isOnline = ref('')
const gameMode = ref('')
const aiDifficulty = ref('')
const players = ref([
  { name1: '', name2: '' },
  { name1: '', name2: '' },
  { name1: '', name2: '' },
  { name1: '', name2: '' }
])

const leaderboard = ref([
  { id: 1, name: 'Jane Smith', score: 1500, status: 'bg-success' },
  { id: 2, name: 'Mike Johnson', score: 1200, status: 'bg-danger' },
  { id: 3, name: 'Emily Davis', score: 1000, status: 'bg-success' },
  { id: 4, name: 'Chris Brown', score: 800, status: 'bg-danger' }
])

const filteredPlayers = computed(() => {
  if (gameMode.value === 'onePlayer' || gameMode.value === 'twoPlayer') {
    return players.value.slice(0, 1)
  } else if (gameMode.value === 'eightPlayer') {
    return players.value
  }
  return []
})

const emit = defineEmits(['startGame'])

const setGameMode = (mode) => {
  isOnline.value = mode
  gameMode.value = ''
}

const startGame = () => {
  const data = {
    gameMode: gameMode.value,
    players: players.value.map((player) => ({
      player1Name: player.name1,
      player2Name: player.name2
    }))
  }

  if (gameMode.value === 'onePlayer') {
    data.aiDifficulty = aiDifficulty.value
  }

  emit('startGame', data)
}
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  padding-top: 100px;
}

.form-content {
  background-color: #f9f9f9;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 500px;
  font-family: Titulo, sans-serif;
}

.title {
  font-family: Titulo, sans-serif;
  font-size: 2rem;
  color: #007bff;
  margin-bottom: 1.5rem;
  text-align: center;
}
.OnlineTitle {
  font-family: Titulo, sans-serif;
  font-size: 1rem;
  color: #007bff;
  margin-bottom: 1.5rem;
  text-align: center;
}
.game-form {
  width: 100%;
}

.toggle-btn {
  font-size: 1.2rem;
  font-weight: bold;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
}

.mode-toggle {
  gap: 20px;
}

.player-inputs {
  margin-top: 1.5rem;
}

.player-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}

.player-input {
  padding: 0.8rem;
  border-radius: 12px;
  font-size: 1rem;
  background-color: #eef2f7;
  border: 1px solid #ced4da;
}

.player-input:focus {
  border-color: #007bff;
}

.vs-text {
  font-weight: bold;
  font-size: 1.2rem;
  color: #495057;
  margin: 0 10px;
}

.ai-difficulty select {
  padding: 0.5rem;
  border-radius: 10px;
  background-color: #f8f9fa;
}

.submit-btn {
  background-color: #007bff;
  border-radius: 12px;
  font-size: 1.25rem;
  font-family: Titulo, sans-serif;
}

.leaderboard-container {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.leaderboard {
  background-color: #2c3e50;
  padding: 1.5rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 500px;
}

.leaderboard-title {
  font-family: Titulo, sans-serif;
  font-size: 1.5rem;
  color: #ecf0f1;
  text-align: center;
  margin-bottom: 1rem;
}

.list-group-item {
  background-color: #34495e;
  border-radius: 12px;
  color: #ecf0f1;
  border: none;
  margin-bottom: 0.5rem;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
}

.bg-success {
  background-color: #27ae60;
}

.bg-danger {
  background-color: #e74c3c;
}

.trophy-image {
  width: 150px;
  height: auto;
}

.trophy-container {
  margin-top: 2rem;
}
</style>
