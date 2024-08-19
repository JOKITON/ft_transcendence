<script setup>
import { ref, markRaw } from 'vue';
import NavHome from "../NavHome.vue";
import PongAI from "./PongAI.vue";
import Pong2P from "./Pong2P.vue";
import PongTournament from "./PongTournament.vue"; // Assuming you have a component for the tournament mode
import NameInputMenu from "./NameInputMenu.vue";

// Define the reactive properties
const showMenu = ref(true);
const selectedGame = ref(null);  // This will hold 'PongAI', 'Pong2P', or 'PongTournament'
const player1Name = ref('');
const player2Name = ref('');
const player3Name = ref('');
const player4Name = ref('');
const player5Name = ref('');
const player6Name = ref('');
const player7Name = ref('');
const player8Name = ref('');

// Function to handle the game start event
const handleStartGame = (data) => {
  let gameMode = data.gameMode;

  // Store player names based on the game mode
  player1Name.value = data.player1Name || '';
  player2Name.value = data.player2Name || '';
  player3Name.value = data.player3Name || '';
  player4Name.value = data.player4Name || '';
  player5Name.value = data.player5Name || '';
  player6Name.value = data.player6Name || '';
  player7Name.value = data.player7Name || '';
  player8Name.value = data.player8Name || '';

  // Determine which game component to use based on the selected game mode
  if (gameMode === 'onePlayer') {
    selectedGame.value = markRaw(PongAI);
  } else if (gameMode === 'twoPlayer') {
    selectedGame.value = markRaw(Pong2P);
  } else if (gameMode === 'eightPlayer') {
    selectedGame.value = markRaw(PongTournament);
  }

  // Hide the menu and show the selected game
  showMenu.value = false;
};

// Function to handle returning to the main menu
const returnToMenu = () => {
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
      :player1Name="player1Name" 
      :player2Name="player2Name"
      :player3Name="player3Name"
      :player4Name="player4Name"
      :player5Name="player5Name"
      :player6Name="player6Name"
      :player7Name="player7Name"
      :player8Name="player8Name"
      @returnToMenu="returnToMenu"
    />
  </div>
</template>
