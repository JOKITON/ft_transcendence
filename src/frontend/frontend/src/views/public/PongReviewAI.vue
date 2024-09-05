<script setup lang="ts">

import { Vector3, Color, Mesh } from 'three';
import { onMounted, onBeforeUnmount, ref } from 'vue';
import ThreeService from '../../services/pong/ThreeService';
import Player from '../../services/pong/Player';
import Sphere from '../../services/pong/Objects/Sphere';
import DashedWall from '../../services/pong/Objects/DashedWall';
import Score from '../../services/pong/Objects/Score';
import HelpText from '../../services/pong/Objects/HelpText';
import GameOver from '../../services/pong/Objects/GameOver';
import Wall from '../../services/pong/Wall';
import { handleCollisions } from '../../services/pong/Utils';

const three = new ThreeService(1200, 700);

// Define bounds of the Pong game
const bounds = { minX: -16.2, maxX: 16.2, minY: -9.2, maxY: 9.2, minZ: 0, maxZ: 0 };

// Ball object
const ballVectorY = Math.random() * 0.2 - 0.1;
const ballVelocity = new Vector3(0.05, ballVectorY, 0);
const ballGeometry = [0.33, 10, 10];
const ball = new Sphere(ballGeometry, new Color('white'), new Vector3(0, 0, 0), ballVelocity, bounds);

// Horizontal walls
const vecHorizWall = new Vector3(33, 0.3, 1);
const horizWallUp = new Wall(vecHorizWall, new Vector3(0, 10, 0), new Color('white'));
const horizWallDown = new Wall(vecHorizWall, new Vector3(0, -10, 0), new Color('white'));

// Vertical dashed wall
const vecWallMid = [new Vector3(0, -9, 0), new Vector3(0, 9, 0)];
const dashedLine = [1, 0.66, 0.5];
const wallMid = new DashedWall(vecWallMid, new Color('green'), dashedLine);

// Player objects (to be initialized later)
let playerAIOne: Player;
let playerAITwo: Player;

// Scores
let numScorePlayerOne = 0;
let numScorePlayerTwo = 0;
const scorePlayer1 = new Score(numScorePlayerOne, new Color('white'), new Vector3(-2, 7.5, 0));
const scorePlayerAI = new Score(numScorePlayerTwo, new Color('white'), new Vector3(2, 7.5, 0));

const isAnimating = ref(true);
const isGameOver = ref(false);
const winner = ref('');

// Initialize players with the provided names
playerAIOne = new Player(new Vector3(0.4, 3, 0.5), new Color('red'), new Vector3(-16, 0, 0), '', '', 'AI1');
playerAITwo = new Player(new Vector3(0.4, 3, 0.5), new Color('blue'), new Vector3(16, 0, 0), '', '', 'AI2');
playerAIOne.setAiDifficulty(Number(300));
playerAITwo.setAiDifficulty(Number(300));
playerAIOne.setSpeed(0.5);
playerAITwo.setSpeed(0.5);

// const helpTextSpace = new HelpText('Press space to start', new Color('white'), new Vector3(0, 3.5, 0));

const helpTextPlayerOne = new HelpText('AI', new Color('white'), new Vector3(-16, 3.5, 0));
const helpTextPlayerTwo = new HelpText('AI', new Color('white'), new Vector3(16, 3.5, 0));

function setupScene() {
  three.addScene(helpTextPlayerOne.get());
  three.addScene(helpTextPlayerTwo.get());
  three.addScene(horizWallUp.get());
  three.addScene(horizWallDown.get());
  three.addScene(wallMid.get());
  three.addScene(playerAIOne.get());
  three.addScene(playerAITwo.get());
  three.addScene(ball.get());
  three.addScene(scorePlayer1.get());
  three.addScene(scorePlayerAI.get());

  isAnimating.value = true;
}

function update() {
  setTimeout(() => {
    three.removeScene(helpTextPlayerOne.get());
    three.removeScene(helpTextPlayerTwo.get());
  }, 4000);
  if (!isAnimating.value) {
    setTimeout(() => {
      isAnimating.value = true;
    }, 1000);
    return;
  }

  let check = ball.update();
  if (check) {
    if (check === 1) {
      numScorePlayerTwo += 1;
      scorePlayerAI.updateScore(numScorePlayerTwo);
      blinkObject(playerAITwo.get());
      if (numScorePlayerTwo == 5) {
        console.log(`${playerAIOne.getName()} lost!`);
        endGame(playerAITwo.getName());
      }
      ball.invertVelocity();
    } else if (check === 2) {
      numScorePlayerOne += 1;
      scorePlayer1.updateScore(numScorePlayerOne);
      blinkObject(scorePlayer1.get());
      if (numScorePlayerOne == 5) {
        console.log(`${playerAITwo.getName()} lost!`);
        endGame(playerAIOne.getName());
      }
    } else {
      console.error('Unexpected check value');
    }
    returnObjectsToPlace();
    const ballVectorY = Math.random() * 0.2 - 0.1;
    ball.setVelocityY(ballVectorY);
    isAnimating.value = false;
    setTimeout(() => {
      playerAITwo.returnToPlace();
    }, 300);
    return;
  }

  playerAIOne.updateAI(ball, 10);
  playerAITwo.updateAI(ball, 10);
  handleCollisions(ball, playerAIOne, playerAITwo);
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
  playerAIOne.returnToPlace();
  playerAITwo.returnToPlace();
}

function toggleAnimation(event: KeyboardEvent) {
  if (event.code === 'Space') {
    isAnimating.value = !isAnimating.value;
    console.log(`Animation ${isAnimating.value ? 'resumed' : 'paused'}`);
  }
}

const endGame = (winningPlayer: string) => {
  const finalScore = new GameOver(winningPlayer + ' won!', new Color('white'), new Vector3(0, 0.5, 0));
  three.addScene(finalScore.get());
  blinkObject(finalScore.get());
  setTimeout(() => {
    finalScore.updateScore("Returning to home...");
  }, 2000);
  setTimeout(() => {
    winner.value = winningPlayer;
    isGameOver.value = true;
  }, 5000);
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
  playerAIOne?.dispose();
  playerAITwo?.dispose();
  ball.dispose();
  horizWallDown.dispose();
  horizWallUp.dispose();
  wallMid.dispose();
  scorePlayer1.dispose();
  scorePlayerAI.dispose();
  helpTextPlayerOne.dispose();
  helpTextPlayerTwo.dispose();
});
</script>

<template>
  <div></div>
</template>
