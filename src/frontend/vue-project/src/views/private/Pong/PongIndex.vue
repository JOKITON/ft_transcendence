<script setup>
import { ref } from 'vue';
import NavHome from "../NavHome.vue";
import PongAI from "./PongAI.vue";
import Pong2P from "./Pong2P.vue";
import NameInputMenu from "./NameInputMenu.vue";

// Define the reactive properties
const showMenu = ref(true);
const selectedGame = ref(null);  // This will hold 'PongAI' or 'Pong2P'
const player1Name = ref('');
const player2Name = ref('');

// Function to handle the game start event
const handleStartGame = ({ gameMode, player1Name: p1Name, player2Name: p2Name }) => {
  player1Name.value = p1Name;
  player2Name.value = p2Name || 'AI'; // Use 'AI' as the second player's name for single-player mode

  // Determine which game component to use based on the selected game mode
  if (gameMode === 'onePlayer') {
    selectedGame.value = PongAI;
  } else if (gameMode === 'twoPlayer') {
    selectedGame.value = Pong2P;
  }

  showMenu.value = false;
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
    />
  </div>
</template>
