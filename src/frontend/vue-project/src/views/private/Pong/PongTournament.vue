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

const props = defineProps({
  players: Array<Object>,
});

const emit = defineEmits(['returnToMenu']);

// Index to track the current game in the tournament
let indexGame = 0;

// Extract initial players for the current game
let player1Name = ref(props.players[indexGame].player1Name);
let player2Name = ref(props.players[indexGame].player2Name);

console.log('Players:', props.players[indexGame].player1Name);
props.players.forEach(({ player1Name, player2Name }) => {
  console.log(player1Name);
  console.log(player2Name);
});

const returnToMenu = (winningPlayer: string, losingPlayer: string, semiOne: string, semiTwo: string, semiThree: string, semiFour: string) => {
  emit('returnToMenu', {
    winner: winningPlayer,
    runnerUp: losingPlayer,
    semiFinalists: [semiOne, semiTwo, semiThree, semiFour],
  });
};

const three = new ThreeService(window.innerWidth, window.innerHeight);

// Define bounds of the Pong game
const bounds = { minX: -16.2, maxX: 16.2, minY: -9.2, maxY: 9.2, minZ: 0, maxZ: 0 };

// Ball object
const ballVectorY = Math.random() * 0.2 - 0.1;
const ballVelocity = new Vector3(0.05, ballVectorY, 0);
const ballGeometry = [0.5, 10, 10];
const ball = new Sphere(ballGeometry, new Color('white'), new Vector3(0, 0, 0), ballVelocity, bounds);

// Horizontal walls
const vecHorizWall = new Vector3(33, 0.3, 1);
const horizWallUp = new Wall(vecHorizWall, new Vector3(0, 10, 0), new Color('white'));
const horizWallDown = new Wall(vecHorizWall, new Vector3(0, -10, 0), new Color('white'));

// Vertical dashed wall
const vecWallMid = [new Vector3(0, -9, 0), new Vector3(0, 9, 0)];
const dashedLine = [10, 0.66, 0.5];
const wallMid = new DashedWall(vecWallMid, new Color('green'), dashedLine);

// Scores
let numScorePlayerOne = 0;
let numScorePlayerTwo = 0;
const scorePlayer1 = new Score(numScorePlayerOne, new Color('white'), new Vector3(-2, 7.5, 0));
const scorePlayer2 = new Score(numScorePlayerTwo, new Color('white'), new Vector3(2, 7.5, 0));

const isAnimating = ref(true);
const isGameOver = ref(false);
const winner = ref('');

// Initialize players with the provided names
const player = new Player(new Vector3(0.4, 3, 0.5), new Color('red'), new Vector3(16, 0, 0), 'ArrowUp', 'ArrowDown', player1Name.value);
const player2 = new Player(new Vector3(0.4, 3, 0.5), new Color('blue'), new Vector3(-16, 0, 0), 'KeyW', 'KeyS', player2Name.value);

const helpTextSpace = new HelpText('Press space to start', new Color('white'), new Vector3(0, 3.5, 0));

const helpTextPlayerOne = new HelpText(player1Name.value, new Color('white'), new Vector3(-16, 3.5, 0));
const helpTextPlayerTwo = new HelpText(player2Name.value, new Color('white'), new Vector3(16, 3.5, 0));

function setupScene() {
  setHelpText();
  three.addScene(horizWallUp.get());
  three.addScene(horizWallDown.get());
  three.addScene(wallMid.get());
  three.addScene(player.get());
  three.addScene(player2.get());
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
  }, 4000);
}

function update() {
  if (!isAnimating.value) return;

  const check = ball.update();
  if (check) {
    if (check === 1) {
      numScorePlayerTwo += 1;
      scorePlayer2.updateScore(numScorePlayerTwo);
      blinkObject(scorePlayer2.get());
      if (numScorePlayerTwo === 1) {
        console.log(`${player.getName()} lost!`);
        endGame(player2.getName(), player.getName());
      }
      ball.invertVelocity();
    } else if (check === 2) {
      numScorePlayerOne += 1;
      scorePlayer1.updateScore(numScorePlayerOne);
      blinkObject(scorePlayer1.get());
      if (numScorePlayerOne === 1) {
        console.log(`${player2.getName()} lost!`);
        endGame(player.getName(), player2.getName());
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

  player.update();
  player2.update();
  handleCollisions(ball, player, player2);
}

// Blinking effect for the score when a player loses
function blinkObject(mesh: Mesh) {
  let visible = true;
  const blinkDuration = 800;
  const blinkInterval = 200;

  const intervalId = setInterval(() => {
    visible = !visible;
    mesh.visible = visible;

    setTimeout(() => {
      clearInterval(intervalId);
      mesh.visible = true;
    }, blinkDuration);
  }, blinkInterval);
}

function returnObjectsToPlace() {
  player.returnToPlace();
  player2.returnToPlace();
}

function toggleAnimation(event: KeyboardEvent) {
  if (event.code === 'Space') {
    isAnimating.value = !isAnimating.value;
    console.log(`Animation ${isAnimating.value ? 'resumed' : 'paused'}`);
  }
}

function resetScores(): void {
  scorePlayer1.updateScore(0);
  scorePlayer2.updateScore(0);
  numScorePlayerOne = 0;
  numScorePlayerTwo = 0;
}

let semiOne = '';
let semiTwo = '';
let semiThree = '';
let semiFour = '';

let finalOne = '';
let finalTwo = '';

function manageTournament(winPlayer: string, matchIndex: number): void {
  if (matchIndex === 1) {
    semiOne = winPlayer;
    player1Name.value = props.players[1].player1Name;
    player2Name.value = props.players[1].player2Name;
  } else if (matchIndex === 2) {
    semiTwo = winPlayer;
    player1Name.value = props.players[2].player1Name;
    player2Name.value = props.players[2].player2Name;
  } else if (matchIndex === 3) {
    semiThree = winPlayer;
    player1Name.value = props.players[3].player1Name;
    player2Name.value = props.players[3].player2Name;
  } else if (matchIndex === 4) {
    semiFour = winPlayer;
    player1Name.value = semiOne;
    player2Name.value = semiTwo;
  } else if (matchIndex === 5) {
    finalOne = winPlayer;
    player1Name.value = semiThree;
    player2Name.value = semiFour;
  } else if (matchIndex === 6) {
    finalTwo = winPlayer;
    player1Name.value = finalOne;
    player2Name.value = finalTwo;
  }

  // Update player names for the next match
  player.setName(player1Name.value);
  player2.setName(player2Name.value);
}

const endGame = (winningPlayer: string, losingPlayer: string) => {
  const finalScore = new GameOver(winningPlayer + ' won!', new Color('white'), new Vector3(0, 0.5, 0));
  three.addScene(finalScore.get());
  blinkObject(finalScore.get());
  indexGame += 1;

  if (indexGame < 7) {
    setTimeout(() => {
      three.removeScene(finalScore.get());
      resetScores();
      manageTournament(winningPlayer, indexGame);
      setHelpText();
    }, 5000);
  } else if (indexGame === 7) {
    setTimeout(() => {
      finalScore.updateScore("Returning to home...");
    }, 2000);
    setTimeout(() => {
      winner.value = winningPlayer;
      isGameOver.value = true;
      returnToMenu(winningPlayer, losingPlayer, semiOne, semiTwo, semiThree, semiFour);
    }, 5000);
  }
};

onMounted(() => {
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
  player.dispose();
  player2.dispose();
  ball.dispose();
  scorePlayer1.dispose();
  scorePlayer2.dispose();
});
</script>

<template>
  <div></div>
</template>
