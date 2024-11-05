<script setup lang="ts">
import { Vector3, Color } from 'three';
import { onMounted, onBeforeUnmount, ref } from 'vue';
import ThreeService from 'pong/ThreeService';
import Player from 'pong-objects/Player';
import Sphere from 'pong-objects/Sphere';
import DashedWall from 'pong-objects/Text/DashedWall';
import Score from 'pong-objects/Text/Score';
import HelpText from 'pong-objects/Text/HelpText';
import GameOver from 'pong-objects/Text/GameOver';
import Wall from 'pong-objects/Wall';
import { handleCollisions, blinkObject } from 'pong-utils/Utils';
import LuckySphere from 'pong-objects/LuckySphere';

import {
  type intStatePongData,
  setBallVelocity,
  ballGeometry,
  ballGeometry2,
  ballVelocity,
  vecHorizWall,
  bounds,
  ballVectorY,
  font
} from 'pong-utils/pongVariables'
import {
  IS_STATE,
  IS_COMPLETED,
  SCORE_TO_WIN,
  BIT_FONT,
  MONTSERRAT_FONT
} from 'pong-utils/pongVariables'

const three = new ThreeService(800, 500)

// Ball object
const ball = new Sphere(
  ballGeometry,
  new Color('white'),
  new Vector3(0, 0, 0),
  ballVelocity,
  bounds
)

// Horizontal walls
const horizWallUp = new Wall(vecHorizWall, new Vector3(0, 10, 0), new Color('white'))
const horizWallDown = new Wall(vecHorizWall, new Vector3(0, -10, 0), new Color('white'))

let wallMid: DashedWall // Vertical dashed wall
let scorePlayer1: Score
let scorePlayerAI: Score
let helpText: GameOver

let helpTextSpace: HelpText
let helpTextPlayerOne: HelpText
let helpTextPlayerTwo: HelpText

let helpTextControlsOne: HelpText

let finalScore: GameOver

// Scores
let numScorePlayerOne = 0
let numScorePlayerTwo = 0

async function loadFontObjects() {

  // Vertical dashed wall
  wallMid = new DashedWall('- - - - - - - -', new Color('green'), new Vector3(0, 0, -1), font)

  // Set the text for the score of each player
  scorePlayer1 = new Score(numScorePlayerOne, new Color('white'), new Vector3(-2, 7.5, 0), font)
  scorePlayerAI = new Score(numScorePlayerTwo, new Color('white'), new Vector3(2, 7.5, 0), font)

  // Set the text for the controls
  helpTextControlsOne = new HelpText(
    '↑\n\n\n↓',
    new Color('white'),
    new Vector3(-16, 0, 0),
    MONTSERRAT_FONT,
    1
  )
  // Set text for the start of the game
  helpTextSpace = new HelpText(
    'Press space to start',
    new Color('white'),
    new Vector3(0, 3.5, 0),
    BIT_FONT,
    2
  )

  // Set text for the player names
  helpTextPlayerOne = new HelpText(
    'AI',
    new Color('red'),
    new Vector3(-16, 5.5, 0),
    BIT_FONT,
    1
  )
  helpTextPlayerTwo = new HelpText('AI', new Color('blue'), new Vector3(16, 5.5, 0), BIT_FONT, 1)

  // Set text for the final score
  finalScore = new GameOver('', new Color('white'), new Vector3(0, 0.5, 0), font)
}

// Player objects (to be initialized later)
let playerAIOne: Player
let playerAITwo: Player

const isAnimating = ref(true)
const isGameOver = ref(false)
const winner = ref('')

// Initialize players with the provided names
playerAIOne = new Player(
  new Vector3(0.4, 3, 0.5),
  new Color('red'),
  new Vector3(-16, 0, 0),
  '',
  '',
  'AI1'
)
playerAITwo = new Player(
  new Vector3(0.4, 3, 0.5),
  new Color('blue'),
  new Vector3(16, 0, 0),
  '',
  '',
  'AI2'
)
playerAIOne.setAiDifficulty(Number(300))
playerAITwo.setAiDifficulty(Number(300))
playerAIOne.setSpeed(0.5)
playerAITwo.setSpeed(0.5)

// const helpTextSpace = new HelpText('Press space to start', new Color('white'), new Vector3(0, 3.5, 0));

function setupScene() {
  three.addScene(helpTextPlayerOne.get())
  three.addScene(helpTextPlayerTwo.get())
  three.addScene(horizWallUp.get())
  three.addScene(horizWallDown.get())
  three.addScene(wallMid.get())
  three.addScene(playerAIOne.get())
  three.addScene(playerAITwo.get())
  three.addScene(ball.get())
  three.addScene(scorePlayer1.get())
  three.addScene(scorePlayerAI.get())

  isAnimating.value = true
}
const audio = new Audio('/songs/ball-hit.mp3')

function update() {
  setTimeout(() => {
    three.removeScene(helpTextPlayerOne.get())
    three.removeScene(helpTextPlayerTwo.get())
  }, 4000)
  if (!isAnimating.value) {
    setTimeout(() => {
      isAnimating.value = true
    }, 1000)
    return
  }

  let check = ball.update()
  if (check) {
    if (check === 1) {
      numScorePlayerTwo += 1
      scorePlayerAI.updateScore(numScorePlayerTwo.toString())
      blinkObject(playerAITwo.get())
      if (numScorePlayerTwo == 999) {
        endGame(playerAITwo.getName())
      }
      ball.invertVelocity()
    } else if (check === 2) {
      numScorePlayerOne += 1
      scorePlayer1.updateScore(numScorePlayerOne.toString())
      blinkObject(scorePlayer1.get())
      if (numScorePlayerOne == 999) {
        endGame(playerAIOne.getName())
      }
    } else {
      console.error('Unexpected check value')
    }
    returnObjectsToPlace()
    const ballVectorY = Math.random() * 0.2 - 0.1
    ball.setVelocityY(ballVectorY)
    isAnimating.value = false
    setTimeout(() => {
      playerAITwo.returnToPlace()
    }, 300)
    return
  }

  playerAIOne.updateAI(ball)
  playerAITwo.updateAI(ball)
  handleCollisions(ball, playerAIOne, playerAITwo, audio)
}

function returnObjectsToPlace() {
  playerAIOne.returnToPlace()
  playerAITwo.returnToPlace()
}

function toggleAnimation(event: KeyboardEvent) {
  if (event.code === 'Space') {
    isAnimating.value = !isAnimating.value
  }
}

const endGame = (winningPlayer: string) => {
  finalScore.updateScore(winningPlayer + ' won!')
  three.addScene(finalScore.get())
  blinkObject(finalScore.get())
  setTimeout(() => {
    finalScore.updateScore('Returning to home...')
  }, 2000)
  setTimeout(() => {
    winner.value = winningPlayer
    isGameOver.value = true
  }, 5000)
}

onMounted(async () => {
  await loadFontObjects()
  setupScene()
  three.startAnimation(update)
  window.addEventListener('resize', () => {
    three.resize(window.innerWidth, window.innerHeight)
  })
  window.addEventListener('keydown', toggleAnimation)
})

onBeforeUnmount(() => {
  three.stopAnimation()
  three.dispose()
  playerAIOne?.dispose()
  playerAITwo?.dispose()
  ball.dispose()
  horizWallDown.dispose()
  horizWallUp.dispose()
  wallMid.dispose()
  scorePlayer1.dispose()
  scorePlayerAI.dispose()
  helpTextPlayerOne.dispose()
  helpTextPlayerTwo.dispose()
})
</script>

<template>
  <div></div>
</template>
