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
  ballGeometry,
  ballGeometry2,
  ballVelocity,
  vecHorizWall,
  bounds,
  ballVectorY,
  font,
} from 'pong-utils/pongVariables'
import {
  IS_STATE,
  IS_COMPLETED,
  SCORE_TO_WIN,
  BIT_FONT,
  MONTSERRAT_FONT
} from 'pong-utils/pongVariables'

const props = defineProps<{
  aiDifficulty: number
  hasStateData: intStatePongData
  isAudioEnabled: boolean
  players: Array<{ player: string; id: number }>
}>()

// console.log(props.hasStateData)

const startTime = Date.now() / 1000
let stateTime: number = 0

const emit = defineEmits(['gameOver'])

const player1Name = ref('')
const player2Name = ref('')

// Game variables to emit later
let gamePlayers: Array<string>
let ids: Array<number>
let scores: Array<number>
let playersHits: Array<number>

// Player objects (to be initialized later)
let player: Player
let player2: Player

// Scores
let numScorePlayerOne = 0
let numScorePlayerTwo = 0

const isAnimating = ref(true)
const isGameOver = ref(false)
const winner = ref('')

if (props.hasStateData.check == true) {
  let stateData = props.hasStateData
  console.log('State data:', stateData)
  setStatePongDate(stateData)
} else setInitialValues()

function setStatePongDate(data: intStatePongData) {
  player1Name.value = data.player_names[0]
  player2Name.value = data.player_names[1]
  numScorePlayerOne = data.player_scores[0]
  numScorePlayerTwo = data.player_scores[1]
  stateTime = data.time_played
  gamePlayers = data.player_names
  ids = data.player_ids
}

function setHits() {
  player.setHits(props.hasStateData.player_hits[0])
  player2.setHits(props.hasStateData.player_hits[1])
}

function setInitialValues() {
  player1Name.value = props.players[0].player
  player2Name.value = props.players[1].player
  // console.log('Player:', player1Name.value)
  gamePlayers = [player1Name.value, player2Name.value]
  ids = [props.players[0].id, props.players[1].id]
}

const three = new ThreeService(window.innerWidth, window.innerHeight)

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

const luckySphere = new LuckySphere(ballGeometry2, new Color('yellow'))

let wallMid: DashedWall // Vertical dashed wall
let scorePlayer1: Score
let scorePlayer2: Score

let helpTextSpace: HelpText
let helpTextPlayerOne: HelpText
let helpTextPlayerTwo: HelpText

let helpTextControlsOne: HelpText
let helpTextControlsTwo: HelpText

let finalScore: GameOver

async function loadFont() {

  // Vertical dashed wall
  wallMid = new DashedWall('- - - - - - - -', new Color('green'), new Vector3(0, 0, -1), font)
  scorePlayer1 = new Score(numScorePlayerOne, new Color('white'), new Vector3(-2, 7.5, 0), font)
  scorePlayer2 = new Score(numScorePlayerTwo, new Color('white'), new Vector3(2, 7.5, 0), font)

  // Set the text for the controls
  helpTextControlsOne = new HelpText(
    'W\n\n\n\n\nS',
    new Color('white'),
    new Vector3(-16, 0, 0),
    BIT_FONT,
    1
  )
  helpTextControlsTwo = new HelpText(
    '↑\n\n\n↓',
    new Color('white'),
    new Vector3(16, 0, 0),
    MONTSERRAT_FONT,
    1
  )

  helpTextSpace = new HelpText(
    'Press space to start',
    new Color('white'),
    new Vector3(0, 3.5, 0),
    BIT_FONT,
    1
  )

  // Set text for the player names
  helpTextPlayerOne = new HelpText(
    player1Name.value,
    new Color('blue'),
    new Vector3(-16, 5.5, 0),
    BIT_FONT,
    1
  )
  helpTextPlayerTwo = new HelpText(
    player2Name.value,
    new Color('red'),
    new Vector3(16, 5.5, 0),
    BIT_FONT,
    1
  )

  finalScore = new GameOver('', new Color('white'), new Vector3(0, 0.5, 0), font)
}

// Initialize players with the provided names
player = new Player(
  new Vector3(0.4, 3, 0.5),
  new Color('blue'),
  new Vector3(-16, 0, 0),
  'KeyW',
  'KeyS',
  player1Name.value
)
player2 = new Player(
  new Vector3(0.4, 3, 0.5),
  new Color('red'),
  new Vector3(16, 0, 0),
  'ArrowUp',
  'ArrowDown',
  player2Name.value
)

function setHelpText() {
  helpTextPlayerOne.updateScore(player1Name.value)
  helpTextPlayerTwo.updateScore(player2Name.value)
  three.addScene(helpTextSpace.get())
  three.addScene(helpTextPlayerOne.get())
  three.addScene(helpTextPlayerTwo.get())
  three.addScene(helpTextControlsOne.get())
  three.addScene(helpTextControlsTwo.get())
  setTimeout(() => {
    three.removeScene(helpTextPlayerOne.get())
    three.removeScene(helpTextPlayerTwo.get())
    three.removeScene(helpTextSpace.get())
  }, 3000)
  setTimeout(() => {
    three.removeScene(helpTextControlsOne.get())
    three.removeScene(helpTextControlsTwo.get())
  }, 6000)
}

function setupScene() {
  if (props.hasStateData.check == true) {
    setHits();
  }
  setHelpText()

  three.addScene(horizWallUp.get())
  three.addScene(horizWallDown.get())
  three.addScene(wallMid.get())

  three.addScene(player.get())
  three.addScene(player2.get())
  three.addScene(ball.get())
  three.addScene(scorePlayer1.get())
  three.addScene(scorePlayer2.get())
  three.addScene(luckySphere.get())

  isAnimating.value = false
}

function scoreTracker(score: number) {
  // Player two won the point
  if (score === 1) {
    numScorePlayerTwo += 1
    scorePlayer2.updateScore(numScorePlayerTwo.toString())
    blinkObject(scorePlayer2.get())
    // Player two won the game
    if (numScorePlayerTwo == SCORE_TO_WIN) {
      console.log(`${player.getName()} lost!`)
      endGame(player2.getName())
    } else emitData(IS_STATE)
  } else if (score === 2) {
    // Player one won the point
    numScorePlayerOne += 1
    scorePlayer1.updateScore(numScorePlayerOne.toString())
    blinkObject(scorePlayer1.get())
    // Player one won the game
    if (numScorePlayerOne == SCORE_TO_WIN) {
      console.log(`${player2.getName()} lost!`)
      endGame(player.getName())
    } else emitData(IS_STATE)
  } else {
    console.error('Unexpected check value')
  }
  returnObjectsToPlace()
  isAnimating.value = false
}

let timeElapsed = 0

const audio = new Audio('/songs/ball-hit.mp3')

function update() {
  if (!isAnimating.value) return
  let isTaken: number = 1
  let now = Date.now()

  if (now - timeElapsed > 5000) {
    // Every 5s, the luckySphere will be repositioned
    timeElapsed = now
    luckySphere.randomizePosition()
    three.addScene(luckySphere.get())
    isTaken = 1
  }

  if (isTaken) {
    if (ball.getVelocity()) {
      isTaken = luckySphere.update(ball, player2)
    } else {
      isTaken = luckySphere.update(ball, player)
    }
    if (isTaken) {
      // Afert applying effects remove luckySphere
      three.removeScene(luckySphere.get())
      timeElapsed = now
    }
    isTaken = 0
  }

  let score = ball.update()
  if (score) {
    // Someone scored a point
    scoreTracker(score)
    window.removeEventListener('keydown', toggleAnimation)
    setTimeout(() => {
      window.addEventListener('keydown', toggleAnimation)
    }, 1000)
  }

  player.update()
  player2.update()
  handleCollisions(ball, player, player2, audio)
}

function returnObjectsToPlace() {
  ball.returnToPlace()
  ball.setVelocityY(ballVectorY)
  ball.invertVelocity()
  player.returnToPlace()
  player2.returnToPlace()
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
      // console.log(`Animation ${isAnimating.value ? 'resumed' : 'paused'}`)
    }, 100) // Adjust the timeout as needed (100ms here)
  }
}

function emitData(status: string) {
  setTimeout(() => {
    scores = [numScorePlayerOne, numScorePlayerTwo]
    playersHits = [player.getHits(), player2.getHits()]
    // winner.value = 'none';

    // Emit the tournament data to the parent component
    let time_played = Date.now() / 1000 - startTime + stateTime
    time_played = Math.floor(time_played)
    emit('gameOver', {
      status: status,
      winner: winner.value,
      player_names: gamePlayers,
      player_scores: scores,
      player_ids: ids,
      player_hits: playersHits,
      time_played: time_played,
      tournament_type: '2P'
    })
  }, 1000)
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
  winner.value = winningPlayer
  isGameOver.value = true
  emitData(IS_COMPLETED)
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
  three.stopAnimation()
  three.dispose()
  player?.dispose()
  player2?.dispose()
  ball.dispose()
  horizWallDown.dispose()
  horizWallUp.dispose()
  wallMid.dispose()
  scorePlayer1.dispose()
  scorePlayer2.dispose()
  helpTextPlayerOne.dispose()
  helpTextPlayerTwo.dispose()
})
</script>

<template>
  <div>
    <audio controls autoplay v-if="props.isAudioEnabled == true" ref="songElement" preload="auto" style="display: none">
      <source src="/src/assets/songs/opening-movie.mp3" type="audio/mp3" />
    </audio>
  </div>
  <div></div>
</template>
