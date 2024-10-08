<script setup lang="ts">
import { onMounted, ref, markRaw, inject } from 'vue'
import NavHome from "../NavHome.vue"
import PongAI from "./PongAI.vue"
import Pong2P from "./Pong2P.vue"
import PongTournament from "./PongTournament.vue"
import NameInputMenu from "./NameInputMenu.vue"
import auth from '../../../services/user/services/auth/auth.ts'
import type Api from '@/utils/Api/Api'

// Reactive state variables
const showMenu = ref(true);
const selectedGame = ref(null);
const aiDif = ref(1);
const arPlayers = ref([]); // Initialize as an array
const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)

onMounted(async () => {
  await fetchId();
});

const user = ref({
  id: 0,
});

// Handle game start
const handleStartGame = (data) => {
  const { aiDifficulty, gameMode, players } = data;

  // Store player names and optionally AI difficulty
  aiDif.value = Number(aiDifficulty);
  arPlayers.value = players;

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
};

// Send tournament data to backend
const sendAIData = async (tournamentResults) => {
  try {
    const response = await api.post("pong/ai", tournamentResults);
    // console.log('Data sent successfully:', response.data);
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
    // Change player name to ID
    tournamentResults.id_player1 = 1;
    tournamentResults.id_player2 = user.value.id;
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
const sendTournamentData = async (tournamentResults) => {
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

async function fetchId() {
  try {
    const response = await Auth.whoami();
    user.value = {
      id: response.id,
    };
    // console.log(user.value.id );
  } catch (error: any) {
    console.error('Error fetching user data:', error.message);
  }
}

// Handle returning to the main menu
const handleGameOver = (tournamentResults) => {
  console.log('Tournament Results:', tournamentResults);

  // Send tournament results to backend
  switch (tournamentResults.tournament_type) {
    case '8P':
      sendTournamentData(tournamentResults);
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
};

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
      :aiDifficulty=aiDif
      @gameOver="handleGameOver"
    />
  </div>
</template>
