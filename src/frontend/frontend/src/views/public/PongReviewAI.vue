<script setup lang="ts">
import { Vector2, Vector3, Color, Mesh } from 'three'
import { onMounted, onBeforeUnmount, ref } from 'vue'
import ThreeService from '../../services/pong/ThreeService'
import Player from '../../services/pong/Objects/Player'
import Sphere from '../../services/pong/Objects/Sphere'
import DashedWall from '../../services/pong/Objects/Text/DashedWall'
import Score from '../../services/pong/Objects/Text/Score'
import HelpText from '../../services/pong/Objects/Text/HelpText'
import GameOver from '../../services/pong/Objects/Text/GameOver'
import Wall from '../../services/pong/Objects/Wall'
import { handleCollisions } from '../../services/pong/Objects/Utils/Utils'
import FontService from '../../services/pong/Objects/Text/FontService'

import {
  setBallVelocity,
  dateStart,
  ballGeometry,
  ballGeometry2,
  ballVelocity,
  vecHorizWall,
  bounds
} from '../../services/pong/Objects/Utils/pongVariables'
import { BIT_FONT, MONTSERRAT_FONT } from '../../services/pong/Objects/Utils/pongVariables'

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

const font = ref(undefined)

let wallMid: DashedWall // Vertical dashed wall
let scorePlayer1: Score
let scorePlayerAI: Score
let helpText: GameOver

let helpTextSpace: HelpText
let helpTextPlayerOne: HelpText
let helpTextPlayerTwo: HelpText

let finalScore: GameOver

async function loadFont() {
  await FontService.loadFont('./src/assets/fonts/Bit5x3_Regular.json').then((loadedFont) => {
    const font = loadedFont

    // Vertical dashed wall
    wallMid = new DashedWall('- - - - - - - -', new Color('green'), new Vector3(0, 0, -1), font)
    scorePlayer1 = new Score(numScorePlayerOne, new Color('white'), new Vector3(-2, 7.5, 0), font)
    scorePlayerAI = new Score(numScorePlayerTwo, new Color('white'), new Vector3(2, 7.5, 0), font)
    helpText = new GameOver('You', new Color('white'), new Vector3(-15.5, 3.5, 0), font)

    helpTextSpace = new HelpText(
      'Press space to start',
      new Color('white'),
      new Vector3(0, 3.5, 0),
      BIT_FONT,
      1
    )

    helpTextPlayerOne = new HelpText(
      'AI',
      new Color('white'),
      new Vector3(-16, 3.5, 0),
      BIT_FONT,
      1
    )
    helpTextPlayerTwo = new HelpText('AI', new Color('white'), new Vector3(16, 3.5, 0), BIT_FONT, 1)

    finalScore = new GameOver('', new Color('white'), new Vector3(0, 0.5, 0), font)
  })
}

// Player objects (to be initialized later)
let playerAIOne: Player
let playerAITwo: Player

// Scores
let numScorePlayerOne = 0
let numScorePlayerTwo = 0

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
      if (numScorePlayerTwo == 5) {
        console.log(`${playerAIOne.getName()} lost!`)
        endGame(playerAITwo.getName())
      }
      ball.invertVelocity()
    } else if (check === 2) {
      numScorePlayerOne += 1
      scorePlayer1.updateScore(numScorePlayerOne.toString())
      blinkObject(scorePlayer1.get())
      if (numScorePlayerOne == 5) {
        console.log(`${playerAITwo.getName()} lost!`)
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

// Blinking effect for the score when a player loses
function blinkObject(mesh: Mesh) {
  let visible = true
  const blinkDuration = 800
  const blinkInterval = 200

  const intervalId = setInterval(() => {
    visible = !visible
    mesh.visible = visible

    setTimeout(() => {
      clearInterval(intervalId)
      mesh.visible = true
    }, blinkDuration)
  }, blinkInterval)
}

function returnObjectsToPlace() {
  playerAIOne.returnToPlace()
  playerAITwo.returnToPlace()
}

function toggleAnimation(event: KeyboardEvent) {
  if (event.code === 'Space') {
    isAnimating.value = !isAnimating.value
    console.log(`Animation ${isAnimating.value ? 'resumed' : 'paused'}`)
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
  await loadFont()
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
