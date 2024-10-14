<script setup lang="ts">
import { onMounted, ref, markRaw, inject } from 'vue'
import NavHome from "../NavHome.vue"
import PongAI from "./PongAI.vue"
import Pong2P from "./Pong2P.vue"
import PongTournament from "./PongTournament4P.vue"
import NameInputMenu from "./NameInputMenu.vue"
import auth from '../../../services/user/services/auth/auth.ts'
import type Api from '@/utils/Api/Api'

// Reactive state variables
const showMenu = ref(true);
const selectedGame = ref(null);
const aiDif = ref(1);
const arPlayers = ref([]); // Initialize as an array
let isAudioEnabledTemp : boolean = false;
const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)
const songElement = ref(null);

const user = ref({
  id: 0,
});

let globalIds = ref({
  idPlayerOne: 0,
  idPlayerTwo: 0,
  idPlayerThree: 0,
  idPlayerFour: 0,
  idPlayerFive: 0,
  idPlayerSix: 0,
  idPlayerSeven: 0,
  idPlayerEight: 0,
});

const stopAudio = () => {
  if (songElement.value) {
    songElement.value.pause();
    songElement.value.currentTime = 0;
  }
}

const resumeAudio = () => {
  if (songElement.value) {
    songElement.value.play();
  }
}

// Handle game start
const handleStartGame = (data) => {
  const { id, aiDifficulty, gameMode, players, isAudioEnabled } = data;

  globalIds.value = id;
  // Store player names and optionally AI difficulty
  aiDif.value = Number(aiDifficulty);
  arPlayers.value = players;
  isAudioEnabledTemp = isAudioEnabled;

  // Select appropriate game component
  if (gameMode === 'onePlayer') {
    selectedGame.value = markRaw(PongAI);
  } else if (gameMode === 'twoPlayer') {
    selectedGame.value = markRaw(Pong2P);
  } else if (gameMode === 'eightPlayer') {
    selectedGame.value = markRaw(PongTournament);
  }

  // Hide menu and show game
  showMenu.value = false;
  stopAudio();
};

// Send tournament data to backend
const sendAIData = async (tournamentResults) => {
  try {
    const response = await api.post("pong/ai", tournamentResults);
    console.log('Data sent successfully:', response.data);
  } catch (error) {
    console.error('Error sending data:', error);

    if (error.response) {
      const message = error.response.data.message || 'An error occurred.';
      const errors = error.response.data.errors || {};

      let errorMessage = `Request failed. ${message}`;
      if (Object.keys(errors).length > 0) {
        errorMessage += '\nErrors:\n';
        for (const [field, msgs] of Object.entries(errors)) {
          errorMessage += `${field}: ${msgs.join(', ')}\n`;
        }
      }
      alert(errorMessage);
    } else {
      alert('Request to the backend failed. Please try again later.');
    }
  }
};

// Send tournament data to backend
const send2PData = async (tournamentResults) => {
  try {
    const response = await api.post("pong/2p", tournamentResults);
    console.log('Data sent successfully:', response.data);
  } catch (error) {
    console.error('Error sending data:', error);

    if (error.response) {
      const message = error.response.data.message || 'An error occurred.';
      const errors = error.response.data.errors || {};

      let errorMessage = `Request failed. ${message}`;
      if (Object.keys(errors).length > 0) {
        errorMessage += '\nErrors:\n';
        for (const [field, msgs] of Object.entries(errors)) {
          errorMessage += `${field}: ${msgs.join(', ')}\n`;
        }
      }
      alert(errorMessage);
    } else {
      alert('Request to the backend failed. Please try again later.');
    }
  }
};

// Send tournament data to backend
const sendTournamentData4P = async (tournamentResults) => {
  try {
    const response = await api.post("pong/4p", tournamentResults);
    console.log('Data sent successfully:', response.data);
  } catch (error) {
    console.error('Error sending data:', error);

    if (error.response) {
      const message = error.response.data.message || 'An error occurred.';
      const errors = error.response.data.errors || {};

      let errorMessage = `Request failed. ${message}`;
      if (Object.keys(errors).length > 0) {
        errorMessage += '\nErrors:\n';
        for (const [field, msgs] of Object.entries(errors)) {
          errorMessage += `${field}: ${msgs.join(', ')}\n`;
        }
      }
      alert(errorMessage);
    } else {
      alert('Request to the backend failed. Please try again later.');
    }
  }
};

// Send tournament data to backend
const sendTournamentData8P = async (tournamentResults) => {
  try {
    const response = await api.post("pong/8p", tournamentResults);
    console.log('Data sent successfully:', response.data);
  } catch (error) {
    console.error('Error sending data:', error);

    if (error.response) {
      const message = error.response.data.message || 'An error occurred.';
      const errors = error.response.data.errors || {};

      let errorMessage = `Request failed. ${message}`;
      if (Object.keys(errors).length > 0) {
        errorMessage += '\nErrors:\n';
        for (const [field, msgs] of Object.entries(errors)) {
          errorMessage += `${field}: ${msgs.join(', ')}\n`;
        }
      }
      alert(errorMessage);
    } else {
      alert('Request to the backend failed. Please try again later.');
    }
  }
};

// Handle returning to the main menu
const handleGameOver = (tournamentResults) => {
  console.log('Tournament Results:', tournamentResults);

  // Send tournament results to backend
  switch (tournamentResults.tournament_type) {
    case '8P':
      sendTournamentData8P(tournamentResults);
      break ;
    case '4P':
      sendTournamentData4P(tournamentResults);
      break ;
    case '2P':
      send2PData(tournamentResults);
      break ;
    case 'AI':
      sendAIData(tournamentResults);
      break ;
  }

  // Reset the state to return to the menu
  showMenu.value = true;
  selectedGame.value = null;
  resumeAudio();
};

</script>

<template>
  <NavHome />
  <audio controls autoplay ref="songElement" preload="auto" style="display: none">
    <source src="/src/assets/songs/main-menu.mp3" type="audio/mp3">
  </audio>
  <div v-if="showMenu">
    <NameInputMenu @startGame="handleStartGame" />
  </div>
  <div v-else>
    <!-- Dynamically load the selected game component -->
    <component 
      :is="selectedGame" 
      :players="arPlayers"
      :aiDifficulty="aiDif"
      :isAudioEnabled="isAudioEnabledTemp"
      @gameOver="handleGameOver"
    />
  </div>
</template>
