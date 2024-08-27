<script setup lang="ts">
import { ref, markRaw } from 'vue'
import axios from 'axios'
import NavHome from '../NavHome.vue'
import PongAI from './PongAI.vue'
import Pong2P from './Pong2P.vue'
import PongTournament from './PongTournament.vue'
import NameInputMenu from './NameInputMenu.vue'

// Reactive state variables
const showMenu = ref(true)
const selectedGame = ref(null)
const aiDif = ref(1)
const arPlayers = ref([]) // Initialize as an array

// Handle game start
const handleStartGame = (data) => {
  const { aiDifficulty, gameMode, players } = data

  // Store player names and optionally AI difficulty
  if (data.aiDifficulty) {
    aiDif.value = aiDifficulty
  }
  arPlayers.value = players

  // Select appropriate game component
  if (gameMode === 'onePlayer') {
    selectedGame.value = markRaw(PongAI)
  } else if (gameMode === 'twoPlayer') {
    selectedGame.value = markRaw(Pong2P)
  } else if (gameMode === 'eightPlayer') {
    selectedGame.value = markRaw(PongTournament)
  }

  // Hide menu and show game
  showMenu.value = false
}

// Send tournament data to backend
const sendTournamentData = async (tournamentResults) => {
  try {
    const response = await axios.post('/pong/tournament/', tournamentResults)
    console.log('Data sent successfully:', response.data)
  } catch (error) {
    console.error('Error sending data:', error)

    if (error.response) {
      const message = error.response.data.message || 'An error occurred.'
      const errors = error.response.data.errors || {}

      let errorMessage = `Request failed. ${message}`
      if (Object.keys(errors).length > 0) {
        errorMessage += '\nErrors:\n'
        for (const [field, msgs] of Object.entries(errors)) {
          errorMessage += `${field}: ${msgs.join(', ')}\n`
        }
      }
      alert(errorMessage)
    } else {
      alert('Request to the backend failed. Please try again later.')
    }
  }
}

// Handle returning to the main menu
const handleReturnToMenu = (tournamentResults) => {
  console.log('Tournament Results:', tournamentResults)

  // Send tournament results to backend
  sendTournamentData(tournamentResults)

  // Reset the state to return to the menu
  showMenu.value = true
  selectedGame.value = null
}
</script>

<template>
  <NavHome />
  <div v-if="showMenu">
    <NameInputMenu @startGame="handleStartGame" />
  </div>
  <div v-else>
    <!-- Dynamically load the selected game component -->
    <component
      :is="selectedGame"
      :players="arPlayers"
      :aiDifficulty="aiDif"
      @returnToMenu="handleReturnToMenu"
    />
  </div>
</template>
