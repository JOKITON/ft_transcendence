<script setup lang="ts">
import { Vector3, Color, Mesh } from 'three'
import { onMounted, onBeforeUnmount, ref } from 'vue'
import ThreeService from '../../../services/pong/ThreeService'
import Player from '../../../services/pong/Objects/Player'
import Sphere from '../../../services/pong/Objects/Sphere'
import DashedWall from '../../../services/pong/Objects/Text/DashedWall'
import Score from '../../../services/pong/Objects/Text/Score'
import HelpText from '../../../services/pong/Objects/Text/HelpText'
import GameOver from '../../../services/pong/Objects/Text/GameOver'
import Wall from '../../../services/pong/Objects/Wall'
import { handleCollisions } from '../../../services/pong/Objects/Utils/Utils'
import FontService from '../../../services/pong/Objects/Text/FontService'
import LuckySphere from '../../../services/pong/Objects/LuckySphere'

import {
  setBallVelocity,
  dateStart,
  ballGeometry,
  ballGeometry2,
  ballVelocity,
  vecHorizWall,
  bounds
} from '../../../services/pong/Objects/Utils/pongVariables'
import { BIT_FONT, MONTSERRAT_FONT } from '../../../services/pong/Objects/Utils/pongVariables'

const props = defineProps({
  isAudioEnabled: Boolean,
  players: Array,
  aiDifficulty: Number
})

const three = new ThreeService(window.innerWidth, window.innerHeight)

const emit = defineEmits(['gameOver'])

// Extract initial players for the current game
let player1Name = ref(props.players[0].player)
console.log('Player:', props.players[0].player)

// Ball object
setBallVelocity(props.aiDifficulty)
const ball = new Sphere(
  ballGeometry,
  new Color('white'),
  new Vector3(0, 0, 0),
  ballVelocity,
  bounds
)
const luckySphere = new LuckySphere(ballGeometry2, new Color('yellow'))

const horizWallUp = new Wall(vecHorizWall, new Vector3(0, 10, 0), new Color('white'));
const horizWallDown = new Wall(vecHorizWall, new Vector3(0, -10, 0), new Color('white'));

// Other variables
let wallMid: DashedWall
let scorePlayer1: Score
let scorePlayerAI: Score
let helpText: GameOver

let helpTextSpace: HelpText
let helpTextPlayerOne: HelpText
let helpTextPlayerTwo: HelpText

let helpTextControlsOne: HelpText
let helpTextControlsTwo: HelpText

let finalScore: GameOver

async function loadFont() {
  await FontService.loadFont('./src/assets/fonts/Bit5x3_Regular.json').then((loadedFont) => {
    const font = loadedFont

    // Vertical dashed wall
    wallMid = new DashedWall('- - - - - - - -', new Color('green'), new Vector3(0, 0, -1), font)

    // Set the text for the score of each player
    scorePlayer1 = new Score(numScorePlayerOne, new Color('white'), new Vector3(-2, 7.5, 0), font)
    scorePlayerAI = new Score(numScorePlayerTwo, new Color('white'), new Vector3(2, 7.5, 0), font)

    // Set the text for the game over message
    helpText = new GameOver('You', new Color('white'), new Vector3(-15.5, 3.5, 0), font)

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
      player1Name.value,
      new Color('red'),
      new Vector3(-16, 5.5, 0),
      BIT_FONT,
      1
    )
    helpTextPlayerTwo = new HelpText('AI', new Color('blue'), new Vector3(16, 5.5, 0), BIT_FONT, 1)

    // Set text for the final score
    finalScore = new GameOver('', new Color('white'), new Vector3(0, 0.5, 0), font)
  })
}

// Player objects (to be initialized later)
let player: Player
let playerAI: Player

// Scores
let numScorePlayerOne = 0
let numScorePlayerTwo = 0

const isAnimating = ref(true)
const isGameOver = ref(false)
const winner = ref('')

// Initialize players with the provided names
player = new Player(
  new Vector3(0.4, 3, 0.5),
  new Color('red'),
  new Vector3(-16, 0, 0),
  'ArrowUp',
  'ArrowDown',
  player1Name.value
)
playerAI = new Player(
  new Vector3(0.4, 3, 0.5),
  new Color('blue'),
  new Vector3(16, 0, 0),
  '',
  '',
  'AI'
)
playerAI.setAiDifficulty(Number(props.aiDifficulty))

function setHelpText() {
  helpTextPlayerOne.updateScore(player1Name.value)
  helpTextPlayerTwo.updateScore('AI')
  three.addScene(helpTextSpace.get())
  three.addScene(helpTextPlayerOne.get())
  three.addScene(helpTextPlayerTwo.get())
  three.addScene(helpTextControlsOne.get())
  setTimeout(() => {
    three.removeScene(helpTextPlayerOne.get())
    three.removeScene(helpTextPlayerTwo.get())
    three.removeScene(helpTextSpace.get())
  }, 3000)
  setTimeout(() => {
    three.removeScene(helpTextControlsOne.get())
  }, 6000)
}

function setupScene() {
  setHelpText();

  three.addScene(horizWallUp.get())
  three.addScene(horizWallDown.get())
  three.addScene(wallMid.get())

  three.addScene(player.get())
  three.addScene(playerAI.get())
  three.addScene(ball.get())
  three.addScene(scorePlayer1.get())
  three.addScene(scorePlayerAI.get())
  three.addScene(luckySphere.get())

  isAnimating.value = false
}

let timeElapsed = 0

function update() {
  if (!isAnimating.value) return
  let isTaken: boolean = true
  let now = Date.now()

  if (now - timeElapsed > 5000) {
    timeElapsed = now
    luckySphere.randomizePosition()
    three.addScene(luckySphere.get())
    isTaken = true
  }

  if (isTaken) {
    if (ball.getVelocity().x < 0) {
      isTaken = luckySphere.update(ball, playerAI)
    } else {
      isTaken = luckySphere.update(ball, player)
    }
    if (isTaken) {
      three.removeScene(luckySphere.get())
      timeElapsed = now
    }
    isTaken = false
  }

  let check = ball.update()
  if (check) {
    if (check === 1) {
      numScorePlayerTwo += 1
      scorePlayerAI.updateScore(numScorePlayerTwo)
      blinkObject(scorePlayerAI.get())
      if (numScorePlayerTwo == 5) {
        console.log(`${player.getName()} lost!`)
        endGame(playerAI.getName())
      }
      ball.invertVelocity()
    } else if (check === 2) {
      numScorePlayerOne += 1
      scorePlayer1.updateScore(numScorePlayerOne)
      blinkObject(scorePlayer1.get())
      if (numScorePlayerOne == 1) {
        console.log(`${playerAI.getName()} lost!`)
        endGame(player.getName())
      }
    } else {
      console.error('Unexpected check value')
    }
    returnObjectsToPlace()
    const ballVectorY = Math.random() * 0.2 - 0.1
    ball.setVelocityY(ballVectorY)
    isAnimating.value = false
    setTimeout(() => {
      playerAI.returnToPlace()
    }, 300)
    return
  }

  player.update()
  playerAI.updateAI(ball)
  handleCollisions(ball, player, playerAI)
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
  ball.returnToPlace()
  player.returnToPlace()
  playerAI.returnToPlace()
}

let debounceTimeout: number | undefined

function toggleAnimation(event: KeyboardEvent) {
  if (isGameOver.value) {
    return
  }

  if (event.code === 'Space') {
    // Clear the previous timeout if the event is fired repeatedly
    if (debounceTimeout) {
      clearTimeout(debounceTimeout)
    }

    // Set a delay before executing the function to avoid multiple triggers
    debounceTimeout = window.setTimeout(() => {
      isAnimating.value = !isAnimating.value
      console.log(`Animation ${isAnimating.value ? 'resumed' : 'paused'}`)
    }, 100) // Adjust the timeout as needed (100ms here)
  }
}

const endGame = (winningPlayer: string) => {
  window.removeEventListener('keydown', toggleAnimation)
  three.removeScene(luckySphere.get())
  finalScore.updateScore(winningPlayer + ' wins!')
  three.addScene(finalScore.get())
  blinkObject(finalScore.get())
  setTimeout(() => {
    finalScore.updateScore('Returning to home...')
  }, 2000)
  setTimeout(() => {
    winner.value = winningPlayer
    isGameOver.value = true

    let players = [player1Name.value, 'AI']
    let ids = [props.players[0].id, 0]
    let scores = [numScorePlayerOne, numScorePlayerTwo]
    const dateEnd = Date.now() / 1000
    let playersHits = [player.getHits(), playerAI.getHits()]

    // Emit the tournament data to the parent component
    emit('gameOver', {
      winner: winningPlayer,
      player_names: players,
      player_scores: scores,
      player_ids: ids,
      player_hits: playersHits,
      time_played: Math.floor(dateEnd - dateStart),
      tournament_type: 'AI'
    })
  }, 5000)
}

onMounted(async () => {
  await loadFont()
  setupScene()
  window.addEventListener('resize', () => {
    three.resize(window.innerWidth, window.innerHeight)
  })
  window.addEventListener('keydown', toggleAnimation)
  three.startAnimation(update)
})

onBeforeUnmount(() => {
  three.dispose()
  player?.dispose()
  playerAI?.dispose()
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
  <div>
    <audio
      controls
      autoplay
      v-if="props.isAudioEnabled == true"
      ref="songElement"
      preload="auto"
      style="display: none"
    >
      <source src="/src/assets/songs/opening-movie.mp3" type="audio/mp3" />
    </audio>
  </div>
  <div></div>
</template>
