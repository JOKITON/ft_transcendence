<script setup lang="ts">

import { Vector3, Color, Mesh } from 'three';
import { onMounted, onBeforeUnmount, ref, defineProps } from 'vue';
import ThreeService from '../../../services/pong/ThreeService';
import Player from '../../../services/pong/Player';
import Sphere from '../../../services/pong/Objects/Sphere';
import DashedWall from '../../../services/pong/Objects/DashedWall';
import Score from '../../../services/pong/Objects/Score';
import GameOver from '../../../services/pong/Objects/GameOver';
import Wall from '../../../services/pong/Wall';
import { handleCollisions } from '../../../services/pong/Utils';

const props = defineProps({
  player1Name: String,
  player2Name: String,
  player3Name: String,
  player4Name: String,
  player5Name: String,
  player6Name: String,
  player7Name: String,
  player8Name: String,
});

const emit = defineEmits(['returnToMenu']);
const returnToMenu = () => {
  emit('returnToMenu');
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
let indexGame = 0;
const winner = ref('');

// Initialize players with the provided names
const player = new Player(new Vector3(0.4, 3, 0.5), new Color('red'), new Vector3(16, 0, 0), 'ArrowUp', 'ArrowDown', props.player1Name);
const player2 = new Player(new Vector3(0.4, 3, 0.5), new Color('blue'), new Vector3(-16, 0, 0), 'KeyW', 'KeyS', props.player2Name);

function setupScene() {
  three.addScene(horizWallUp.get());
  three.addScene(horizWallDown.get());
  three.addScene(wallMid.get());
  three.addScene(player.get());
  three.addScene(player2.get());
  three.addScene(ball.get());
  three.addScene(scorePlayer1.get());
  three.addScene(scorePlayer2.get());
}

function update() {
  if (!isAnimating.value) return;

  let check = ball.update();
  if (check) {
    if (check === 1) {
      numScorePlayerTwo += 1;
      scorePlayer2.updateScore(numScorePlayerTwo);
      blinkObject(scorePlayer2.get());
      if (numScorePlayerTwo == 5) {
        console.log(`${player.getName()} lost!`);
        endGame(player2.getName());
      }
      ball.invertVelocity();
    } else if (check === 2) {
      numScorePlayerOne += 1;
      scorePlayer1.updateScore(numScorePlayerOne);
      blinkObject(scorePlayer1.get());
      if (numScorePlayerOne == 5) {
        console.log(`${player2.getName()} lost!`);
        endGame(player.getName());
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
  if (matchIndex == 1) {
    semiOne = winPlayer;
    player.setName(props.player3Name)
    player2.setName(props.player4Name)
  }
  else if (matchIndex == 2) {
    semiTwo = winPlayer;
    player.setName(props.player5Name)
    player2.setName(props.player6Name)
  }
  if (matchIndex == 3) {
    semiThree = winPlayer;
    player.setName(props.player7Name)
    player2.setName(props.player8Name)
  }
  if (matchIndex == 4) {
    semiFour = winPlayer;
    player.setName(semiOne)
    player2.setName(semiTwo)
  }
  if (matchIndex == 5) {
    finalOne = winPlayer;
    player.setName(semiThree)
    player2.setName(semiFour)
  }
  if (matchIndex == 6) {
    finalTwo = winPlayer;
    player.setName(finalOne)
    player2.setName(finalTwo)
  }
}

const endGame = (winningPlayer: string) => {
  const finalScore = new GameOver(winningPlayer + ' won!', new Color('white'), new Vector3(0, 0.5, 0));
  three.addScene(finalScore.get());
  blinkObject(finalScore.get());
  indexGame += 1;

  if (indexGame != 7) {
    setTimeout(() => {
      three.removeScene(finalScore.get());
      resetScores();
    }, 5000);
    manageTournament(winningPlayer, indexGame);
  }
  // Tournament ends
  else if (indexGame == 7) {
    setTimeout(() => {
      finalScore.updateScore("Returning to home...");
    }, 2000);
    setTimeout(() => {
      winner.value = winningPlayer;
      isGameOver.value = true;
      returnToMenu();
    }, 5000);
  }
};

onMounted(() => {
  setupScene()
  three.startAnimation(update)
  window.addEventListener('resize', () => {
    three.resize(window.innerWidth, window.innerHeight);
  });
  window.addEventListener('keydown', toggleAnimation);
});

onBeforeUnmount(() => {
  three.stopAnimation();
  three.dispose();
  player?.dispose();
  player2?.dispose();
  ball.dispose();
  scorePlayer1.dispose();
  scorePlayer2.dispose();
});
</script>

<template>
  <div></div>
</template>
