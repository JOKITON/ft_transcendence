<script setup lang="ts">

import { Vector3, Color, Mesh } from 'three';
import { onMounted, onBeforeUnmount, ref, defineProps, defineEmits } from 'vue';
import ThreeService from '../../../services/pong/ThreeService';
import Player from '../../../services/pong/Player';
import Sphere from '../../../services/pong/Objects/Sphere';
import DashedWall from '../../../services/pong/Objects/DashedWall';
import Score from '../../../services/pong/Objects/Score';
import HelpText from '../../../services/pong/Objects/HelpText';
import GameOver from '../../../services/pong/Objects/GameOver';
import Wall from '../../../services/pong/Wall';
import { handleCollisions } from '../../../services/pong/Utils';
import FontService from '../../../services/pong/Objects/FontService';

const props = defineProps({
  players: Array<Object>,
});

// console.log('Ids: ', props.players[0].id);

const players = props.players;
// console.log('Players: ', players);

const playerCount = props.players.length;
console.log('Player count:', playerCount);

const emit = defineEmits(['gameOver']);

// Index to track the current game in the tournament
let indexGame = 0;

// Extract initial players for the current game
let player1Name = ref(props.players?.[0]?.player || 'Player 1');
let player2Name = ref(props.players?.[1]?.player || 'Player 2');

props.players.forEach((player, index) => {
  if (index % 2 === 0 && index + 1 < props.players.length) {
    const player1 = player;
    const player2 = props.players[index + 1];
    console.log('{', player1.player, '} vs {', player2.player, '}');
  }
});

const three = new ThreeService(window.innerWidth, window.innerHeight);

// Define bounds of the Pong game
const bounds = { minX: -16.2, maxX: 16.2, minY: -9.2, maxY: 9.2, minZ: 0, maxZ: 0 };

// Ball object
const ballVectorY = Math.random() * 0.2 - 0.1;
const ballVelocity = new Vector3(0.5, ballVectorY, 0);
const ballGeometry = [0.5, 10, 10];
const ball = new Sphere(ballGeometry, new Color('white'), new Vector3(0, 0, 0), ballVelocity, bounds);

// Horizontal walls
const vecHorizWall = new Vector3(33, 0.3, 1);
const horizWallUp = new Wall(vecHorizWall, new Vector3(0, 10, 0), new Color('white'));
const horizWallDown = new Wall(vecHorizWall, new Vector3(0, -10, 0), new Color('white'));

const font = ref(undefined);

let wallMid: DashedWall; // Vertical dashed wall
let scorePlayer1: Score;
let scorePlayer2: Score;
let helpText: GameOver;

let helpTextSpace: HelpText;
let helpTextPlayerOne: HelpText;
let helpTextPlayerTwo: HelpText;

let finalScore: GameOver;

async function loadFont() {
  await FontService.loadFont('./src/assets/fonts/Bit5x3_Regular.json').then((font) => {
    font.value = font;  

    // Vertical dashed wall
    wallMid = new DashedWall("- - - - - - - -", new Color('green'), new Vector3(0, 0, -1), font.value);
    scorePlayer1 = new Score(variableScoreOne, new Color('white'), new Vector3(-2, 7.5, 0), font.value);
    scorePlayer2 = new Score(variableScoreTwo, new Color('white'), new Vector3(2, 7.5, 0), font.value);
    helpText = new GameOver('You', new Color('white'), new Vector3(-15.5, 3.5, 0), font.value);

    helpTextSpace = new HelpText('Press space to start', new Color('white'), new Vector3(0, 3.5, 0));

    helpTextPlayerOne = new HelpText(player1Name.value, new Color('white'), new Vector3(-16, 3.5, 0));
    helpTextPlayerTwo = new HelpText('AI', new Color('white'), new Vector3(16, 3.5, 0));

    finalScore = new GameOver('', new Color('white'), new Vector3(0, 0.5, 0), font.value);
  });
}

// Scores
let variableScoreOne = 0;
let variableScoreTwo = 0;
let playerScores: Array<Array<number>>= [[]];
playerScores = Array.from({ length: playerCount }, () => []);

let posPlayers: Array<number> = new Array(8).fill(0);  // Assuming an array of size 8

const isAnimating = ref(true);
const isGameOver = ref(false);
const winner = ref('');

// Initialize players with the provided names
const playerOne = new Player(new Vector3(0.4, 3, 0.5), new Color('red'), new Vector3(16, 0, 0), 'ArrowUp', 'ArrowDown', player1Name.value);
const playerTwo = new Player(new Vector3(0.4, 3, 0.5), new Color('blue'), new Vector3(-16, 0, 0), 'KeyW', 'KeyS', player2Name.value);


function setupScene() {
  setHelpText();
  three.addScene(horizWallUp.get());
  three.addScene(horizWallDown.get());
  three.addScene(wallMid.get());
  three.addScene(playerOne.get());
  three.addScene(playerTwo.get());
  three.addScene(ball.get());
  three.addScene(scorePlayer1.get());
  three.addScene(scorePlayer2.get());

  isAnimating.value = false;
}

function setHelpText() {
  helpTextPlayerOne.updateScore(player1Name.value);
  helpTextPlayerTwo.updateScore(player2Name.value);
  three.addScene(helpTextSpace.get());
  three.addScene(helpTextPlayerOne.get());
  three.addScene(helpTextPlayerTwo.get());
  setTimeout(() => {
    three.removeScene(helpTextPlayerOne.get());
    three.removeScene(helpTextPlayerTwo.get());
    three.removeScene(helpTextSpace.get());
  }, 3000);
}

function update() {
  if (!isAnimating.value) return;

  const check = ball.update();
  if (check) {
    if (check === 1) {
      variableScoreTwo += 1;
      scorePlayer2.updateScore(variableScoreTwo);
      blinkObject(scorePlayer2.get());
      if (variableScoreTwo === 1) {
        console.log(`${playerOne.getName()} lost!`);
        endGame(playerTwo.getName(), playerOne.getName());
      }
      ball.invertVelocity();
    } else if (check === 2) {
      variableScoreOne += 1;
      scorePlayer1.updateScore(variableScoreOne);
      blinkObject(scorePlayer1.get());
      if (variableScoreOne === 1) {
        console.log(`${playerTwo.getName()} lost!`);
        endGame(playerOne.getName(), playerTwo.getName());
      }
    } else {
      console.error('Unexpected check value');
    }
    returnObjectsToPlace();
    const ballVectorY = Math.random() * 0.2 - 0.1;
    ball.setVelocityY(ballVectorY);
    isAnimating.value = false;
    return;
  }

  playerOne.update();
  playerTwo.update();
  handleCollisions(ball, playerOne, playerTwo);
}

// Blinking effect for the score when a player loses
function blinkObject(mesh: Mesh) {
  let visible = true;
  const blinkDuration = 800;
  const blinkInterval = 200;

  const intervalId = setInterval(() => {
    visible = !visible;
    mesh.visible = visible;
  }, blinkInterval);

  setTimeout(() => {
    clearInterval(intervalId);
    mesh.visible = true;  // Ensure the mesh is visible after blinking ends
  }, blinkDuration);

}

function returnObjectsToPlace() {
  playerOne.returnToPlace();
  playerTwo.returnToPlace();
}

let debounceTimeout: number | undefined;

function toggleAnimation(event: KeyboardEvent) {
  if (isGameOver.value) {
    return;
  }

  if (event.code === 'Space') {
    // Clear the previous timeout if the event is fired repeatedly
    if (debounceTimeout) {
      clearTimeout(debounceTimeout);
    }

    // Set a delay before executing the function to avoid multiple triggers
    debounceTimeout = setTimeout(() => {
      isAnimating.value = !isAnimating.value;
      console.log(`Animation ${isAnimating.value ? 'resumed' : 'paused'}`);
    }, 100);
  }
}

function resetScores(): void {
  scorePlayer1.updateScore(0);
  scorePlayer2.updateScore(0);
  variableScoreOne = 0;
  variableScoreTwo = 0;
}

/* Player positions */
let finalOne = '';
let finalTwo = '';

// Simplified function to update player names
function setNewTournamentNames(newPlayer1Name: string, newPlayer2Name: string): void {
  player1Name.value = newPlayer1Name;
  player2Name.value = newPlayer2Name;
}

// Function to handle semi-final position updates
function setSemiPositions(indexPosPlayer: number, posPlayer: number, losingPlayer: string): void {
  const player1 = player1Name.value;
  const player2 = player2Name.value;

  if (losingPlayer === player1) {
    posPlayers[indexPosPlayer] = posPlayer;
    console.log(`Player: ${player1}, IndexPos: ${indexPosPlayer}, Position: ${posPlayer}`);
  } else if (losingPlayer === player2) {
    posPlayers[indexPosPlayer + 1] = posPlayer;
    console.log(`Player: ${player2}, IndexPos: ${indexPosPlayer + 1}, Position: ${posPlayer}`);
  }
}

// Function to handle final match position updates
function setFinalPositions(losingPlayer: string, indexMatch: number): void {
  console.log(`Setting final position for: ${losingPlayer}, Match Index: ${indexMatch}`);
  const playerIndex = props.players.findIndex(data => // Find the player index
    data.player === losingPlayer || data.player === losingPlayer
  );

  console.log(`Player Index Found: ${playerIndex}`);
  if (playerIndex !== -1) {
    posPlayers[playerIndex] = indexMatch;
    console.log(`Player: ${losingPlayer}, IndexPos: ${playerIndex}, Position: ${indexMatch}`);
  } else {
    console.error(`Player ${losingPlayer} not found in the tournament`);
  }
}

function setFinalNames(  ) {
  player1Name.value = finalOne;
  player2Name.value = finalTwo;
}


// Main function to manage the tournament flow
function manageTournament(winPlayer: string, losingPlayer: string, matchIndex: number): void {
  console.log(`Results: {${variableScoreOne}} {${variableScoreTwo}}`);

  const updateScoresAndNames = (oldPlayerIndex: number, newPlayerIndex: number) => {
    playerScores[oldPlayerIndex].push(variableScoreOne);
    playerScores[oldPlayerIndex + 1].push(variableScoreTwo);

    // Set the semi-final positions
    setSemiPositions(oldPlayerIndex, 5 - matchIndex, losingPlayer);

    // If the match is the final, set the final names
    if (newPlayerIndex == -1)
      setFinalNames();
    // Set the next match players
    else {
      player1Name.value = props.players[newPlayerIndex].player;
      player2Name.value = props.players[newPlayerIndex + 1].player;
    }
  };

  switch (matchIndex) {
    case 1:
      finalOne = winPlayer;
      updateScoresAndNames(0, 2);
      break;
    case 2:
      finalTwo = winPlayer;
      updateScoresAndNames(2, -1);
      break;
    default:
      console.error('Invalid match index');
      break;
  }

  playerTwo.setName(player2Name.value);
  playerOne.setName(player1Name.value);
}

const endGame = (winningPlayer: string, losingPlayer: string) => {
  // Remove the ability to start the game for a short period
  window.removeEventListener("keydown", toggleAnimation);
  three.addScene(finalScore.get());
  finalScore.updateScore(winningPlayer + ' wins!');
  blinkObject(finalScore.get());
  isAnimating.value = false;
  
  indexGame += 1;
  if (indexGame < (playerCount - 1)) {
    manageTournament(winningPlayer, losingPlayer, indexGame);
    setTimeout(() => {
      three.removeScene(finalScore.get());
      window.addEventListener("keydown", toggleAnimation);
      resetScores();
      setHelpText();
    }, 2000);
  } else if (indexGame === (playerCount - 1)) {
    const updatePlayerScores = (player: string, score: number) => {
      const playerIndex = players.findIndex(p => p.player === player);
      if (playerIndex !== -1) {
        playerScores[playerIndex].push(score);
      }
    };

    updatePlayerScores(winningPlayer, variableScoreOne);
    updatePlayerScores(losingPlayer, variableScoreTwo);

    setFinalPositions(losingPlayer, 2);
    setFinalPositions(winningPlayer, 1);

    setTimeout(() => {
      finalScore.updateScore("Returning to home...");
    }, 2000);
    winner.value = winningPlayer;
    isGameOver.value = true;
    setTimeout(() => {

      const tournament_type = playerCount === 4 ? '4P' : '8P';

      // Emit the tournament data to the parent component
      emit('gameOver', {
        players: players.map((player, index) => ({
          id: props.players[index].id,
          name: player.player,
          scores: playerScores[index],
          position: posPlayers[index],
        })),
        final_round: {
          player_one: finalOne,
          player_two: finalTwo,
          winner: winningPlayer,
          loser: losingPlayer,
        },
        tournament_type: tournament_type,
      });
      window.addEventListener("keydown", toggleAnimation);
    }, 5000);
  }
};

onMounted(async () => {
  await loadFont();
  setupScene();
  three.startAnimation(update);
  window.addEventListener('resize', () => {
    three.resize(window.innerWidth, window.innerHeight);
  });
  window.addEventListener('keydown', toggleAnimation);
});

onBeforeUnmount(() => {
  three.stopAnimation();
  three.dispose();
  playerOne?.dispose();
  playerTwo?.dispose();
  ball.dispose();
  horizWallDown.dispose();
  horizWallUp.dispose();
  wallMid.dispose();
  scorePlayer1.dispose();
  scorePlayer2.dispose();
  helpTextPlayerOne.dispose();
  helpTextPlayerTwo.dispose();
  window.removeEventListener('resize', () => {
    three.resize(window.innerWidth, window.innerHeight);
  });
  window.removeEventListener('keydown', toggleAnimation);
});
</script>

<template>
  <div></div>
</template>
