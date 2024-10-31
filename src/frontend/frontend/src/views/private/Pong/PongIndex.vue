<script setup lang="ts">
import { onMounted, ref, markRaw, inject } from 'vue'
import NavHome from '../NavHome.vue'
import PongAI from './PongAI.vue'
import Pong2P from './Pong2P.vue'
import PongTournament from './PongTournament4P.vue'
import NameInputMenu from './NameInputMenu.vue'
import auth from '../../../services/user/services/auth/auth.ts'
import type Api from '@/utils/Api/Api'

// Reactive state variables
const showMenu = ref(true)
const selectedGame = ref(null)
const aiDif = ref(1)
const arPlayers = ref([]) // Initialize as an array
let isAudioEnabledTemp: boolean = false
const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)
const songElement = ref(null)
const statePongData = ref<intStatePongData>({
  check: false,
  id: 0,
  status: '',
  tournament_type: '',
  player_ids: [],
  player_names: [],
  player_scores: [],
  player_hits: [],
  time_played: 0
})

const user = ref({
  id: 0
})

interface intStatePongData {
  check: boolean
  id: number
  status: string
  tournament_type: string
  player_ids: Array<number>
  player_names: Array<string>
  player_scores: Array<number>
  player_hits: Array<number>
  time_played: number
  // aiDifficulty: number,
  // isAudioEnabled: boolean,
}

const stopAudio = () => {
  if (songElement.value) {
    songElement.value.pause()
    songElement.value.currentTime = 0
  }
}

const resumeAudio = () => {
  if (songElement.value) {
    songElement.value.play()
  }
}

// Handle game start
const handleStartGame = async (data) => {
  const { aiDifficulty, gameMode, players, isAudioEnabled } = data

  // Set variables to default values
  statePongData.value = {
    check: false,
    id: 0,
    status: '',
    tournament_type: '',
    player_ids: [],
    player_names: [],
    player_scores: [],
    player_hits: [],
    time_played: 0
  }
  await fetchStateData(gameMode, players)
  if (statePongData.value.tournament_type === gameMode) statePongData.value.check = true
  // gameMode == statePongData?.tournament_type

  // Store player names and optionally AI difficulty
  aiDif.value = Number(aiDifficulty)
  arPlayers.value = players
  isAudioEnabledTemp = isAudioEnabled

  // console.log(arPlayers.value)

  // Select appropriate game component
  if (gameMode === 'AI') {
    selectedGame.value = markRaw(PongAI)
  } else if (gameMode === '2P') {
    selectedGame.value = markRaw(Pong2P)
  } else if (gameMode === '4P') {
    selectedGame.value = markRaw(PongTournament)
  }

  // Hide menu and show game
  showMenu.value = false
  stopAudio()
}

const IS_STATE = 'P'
const IS_COMPLETED = 'C'

const fetchStateData = async (gameMode: string, players) => {
  try {
    const responseWhoAmI = await Auth.whoami()
    user.value.id = responseWhoAmI.id
    let responseState;
    if (gameMode == 'AI' || gameMode == '4P') {
      responseState = await api.get<intStatePongData>(
        '/pong/get-state/' + gameMode + '/' + user.value.id + '/'
      )
    }
    else if (gameMode == '2P') {
      responseState = await api.get<intStatePongData>(
        '/pong/get-state/' + gameMode + '/' + user.value.id + '/' + players[1].id + '/'
      )
    }
    if (responseState.data) {
      statePongData.value = responseState.data
    } else if (responseState.data === undefined) {
      console.log('There is no state data, all good.')
      return
    }
    return true
  } catch (error: any) {
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
    } else if (error.message) {
      alert(`Request failed. ${error.message}`)
    } else {
      alert('Request to the backend failed. Please try again later.')
    }
  }
}

// Send tournament data to backend
const sendPongData = async (tournamentResults) => {
  try {
    let url: string
    switch (tournamentResults.tournament_type) {
      case '2P':
        url = 'pong/2p'
        break
      case 'AI':
        url = 'pong/ai'
        break
    }
    if (tournamentResults.status === IS_STATE) {
      url = 'pong/post-state'
    }
    const response = await api.post(url, tournamentResults)
    console.log('Data sent successfully:', response.data)
  } catch (error: any) {
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

// Send tournament data to backend
const sendTournamentData4P = async (tournamentResults) => {
  try {
    let url: string = 'pong/4p'
    if (tournamentResults.status === IS_STATE) {
      url = 'pong/4p/post-state'
    }
    console.log('Data to send:', tournamentResults)
    await api.post(url, tournamentResults)
    // console.log('Data sent successfully.')
  } catch (error: any) {
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

// Send tournament data to backend
const sendTournamentData8P = async (tournamentResults) => {
  try {
    const response = await api.post('pong/8p', tournamentResults)
    console.log('Data sent successfully:', response.data)
  } catch (error: any) {
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
const handleGameOver = async (tournamentResults) => {
  // Send tournament results to backend
  switch (tournamentResults.tournament_type) {
    case '8P':
      await sendTournamentData8P(tournamentResults)
      break
    case '4P':
      await sendTournamentData4P(tournamentResults)
      break
    default:
      await sendPongData(tournamentResults)
      break
  }

  if (tournamentResults.status === IS_COMPLETED) {
    console.log('Tournament Results:', tournamentResults)
    showMenu.value = true
    selectedGame.value = null
    resumeAudio()
  }
}
</script>

<template>
  <div class="pruebas">
    <NavHome></NavHome>
    <audio controls autoplay ref="songElement" preload="auto" style="display: none">
      <source src="/src/assets/songs/main-menu.mp3" type="audio/mp3" />
    </audio>
  </div>
  <div v-if="showMenu">
    <NameInputMenu @startGame="handleStartGame" />
  </div>
  <div v-else>
    <!-- Dynamically load the selected game component -->
    <component
      :hasStateData="statePongData"
      :is="selectedGame"
      :players="arPlayers"
      :aiDifficulty="aiDif"
      :isAudioEnabled="isAudioEnabledTemp"
      @gameOver="handleGameOver"
    />
  </div>
</template>

<style>
.pruebas {
  position: relative;
  z-index: 100;
}
</style>
