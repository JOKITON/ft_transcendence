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
import { blinkObject, handleCollisions } from '../../../services/pong/Objects/Utils/Utils'
import FontService from '../../../services/pong/Objects/Text/FontService'
import LuckySphere from '../../../services/pong/Objects/LuckySphere'

import {
  type intStatePongData,
  ballGeometry,
  ballGeometry2,
  ballVelocity,
  vecHorizWall,
  bounds,
  ballVectorY
} from '../../../services/pong/Objects/Utils/pongVariables'
import {
  IS_STATE,
  IS_COMPLETED,
  SCORE_TO_WIN,
  BIT_FONT,
  MONTSERRAT_FONT
} from '../../../services/pong/Objects/Utils/pongVariables'

const emit = defineEmits(['gameOver'])

const props = defineProps({
  players: Array<Object>
})
const players = props.players
const playerCount: number = players.length

// Data to return
let ids: Array<number>
let player_names: Array<string>
let player_scores: Array<Array<number>> = [[]]
let startTime: number
let stateTime: number = 0

ids = players.map((player) => player.id)
player_names = players.map((player) => player.player)
player_scores = Array.from({ length: playerCount }, () => Array(1).fill(0))
startTime = Date.now() / 1000

/* 
console.log('Ids: ', ids);
console.log('Player names: ', player_names);
 */

/* console.log('Player count:', playerCount) */

// Extract initial players for the current game
let player1Name = ref(player_names[0])
let player2Name = ref(player_names[1])

// To store scores of each player
let numScorePlayerOne = 0
let numScorePlayerTwo = 0

/* Player positions */
let finalOne = ''
let finalTwo = ''
let winner : string | null = null
let loser : string | null = null

// Reactive variables
const isAnimating = ref(true)
const isGameOver = ref(false)

/*
// Print all the player matches
players.forEach((player, index) => {
  if (index % 2 === 0 && index + 1 < playerCount) {
    const player1 = player
    const player2 = players[index + 1]
    console.log('{', player1.player, '} vs {', player2.player, '}')
  }
})
*/

const three = new ThreeService(window.innerWidth, window.innerHeight)

const horizWallUp = new Wall(vecHorizWall, new Vector3(0, 10, 0), new Color('white'))
const horizWallDown = new Wall(vecHorizWall, new Vector3(0, -10, 0), new Color('white'))

const ball = new Sphere(
  ballGeometry,
  new Color('white'),
  new Vector3(0, 0, 0),
  ballVelocity,
  bounds
)

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
  await FontService.loadFont('./src/assets/fonts/Bit5x3_Regular.json').then((loadedFont) => {
    const font = loadedFont

    // Vertical dashed wall
    wallMid = new DashedWall('- - - - - - - -', new Color('green'), new Vector3(0, 0, -1), font)
    scorePlayer1 = new Score(numScorePlayerOne, new Color('white'), new Vector3(-2, 7.5, 0), font)
    scorePlayer2 = new Score(numScorePlayerTwo, new Color('white'), new Vector3(2, 7.5, 0), font)

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

    finalScore = new GameOver('', new Color('white'), new Vector3(0, 0.5, 0), font)
  })
}

let player_hits: Array<number> = new Array(playerCount).fill(0)

let posPlayers: Array<number> = new Array(8).fill(0) // Assuming an array of size 8

// Initialize players with the provided names
const playerOne = new Player(
  new Vector3(0.4, 3, 0.5),
  new Color('red'),
  new Vector3(16, 0, 0),
  'ArrowUp',
  'ArrowDown',
  player1Name.value
)
const playerTwo = new Player(
  new Vector3(0.4, 3, 0.5),
  new Color('blue'),
  new Vector3(-16, 0, 0),
  'KeyW',
  'KeyS',
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
  setHelpText()
  three.addScene(horizWallUp.get())
  three.addScene(horizWallDown.get())
  three.addScene(wallMid.get())
  three.addScene(playerOne.get())
  three.addScene(playerTwo.get())
  three.addScene(ball.get())
  three.addScene(scorePlayer1.get())
  three.addScene(scorePlayer2.get())
  three.addScene(luckySphere.get())

  isAnimating.value = false
}

function scoreTracker(score: number) {
  updatePlayerData(IS_STATE)
  // Player two won the point
  if (score === 1) {
    numScorePlayerTwo += 1
    scorePlayer2.updateScore(numScorePlayerTwo)
    blinkObject(scorePlayer2.get())
    // Player two won the game
    if (numScorePlayerTwo === SCORE_TO_WIN) {
      console.log(`${playerOne.getName()} lost!`)
      endGame(playerTwo.getName(), playerOne.getName())
    }
    else emitData(IS_STATE);
  } else if (score === 2) {
    // Player one won the point
    numScorePlayerOne += 1
    scorePlayer1.updateScore(numScorePlayerOne)
    blinkObject(scorePlayer1.get())
    // Player one won the game
    if (numScorePlayerOne === SCORE_TO_WIN) {
      console.log(`${playerTwo.getName()} lost!`)
      endGame(playerOne.getName(), playerTwo.getName())
    }
    else emitData(IS_STATE);
  } else {
    console.error('Unexpected check value')
  }
  returnObjectsToPlace()
  isAnimating.value = false
  return
}

let timeElapsed = 0

function update() {
  if (!isAnimating.value) return
  let isTaken: boolean = true // Variable that works as semaphore for luckySphere
  let now = Date.now()

  if (now - timeElapsed > 5000) {
    // Every 5s, the luckySphere will be repositioned
    timeElapsed = now
    luckySphere.randomizePosition()
    three.addScene(luckySphere.get())
    isTaken = true
  }

  if (isTaken) {
    if (ball.getVelocity().x < 0) {
      isTaken = luckySphere.update(ball, playerTwo)
    } else {
      isTaken = luckySphere.update(ball, playerOne)
    }
    if (isTaken) {
      // Afert applying effects remove luckySphere
      three.removeScene(luckySphere.get())
      timeElapsed = now
    }
    isTaken = false
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

  playerOne.update()
  playerTwo.update()
  handleCollisions(ball, playerOne, playerTwo)
}

function returnObjectsToPlace() {
  ball.returnToPlace()
  ball.setVelocityY(ballVectorY)
  ball.invertVelocity()
  playerOne.returnToPlace()
  playerTwo.returnToPlace()
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
    debounceTimeout = setTimeout(() => {
      isAnimating.value = !isAnimating.value
      console.log(`Animation ${isAnimating.value ? 'resumed' : 'paused'}`)
    }, 100)
  }
}

function resetScores(): void {
  scorePlayer1.updateScore(0)
  scorePlayer2.updateScore(0)
  numScorePlayerOne = 0
  numScorePlayerTwo = 0
}

let userIndex = 0;
// Function to handle semi-final position updates
function setSemiPositions(losingPlayer: string): void {
  const player1 = player1Name.value
  const player2 = player2Name.value
  const posPlayer = (5 - indexGame)

  if (losingPlayer === player1) {
    posPlayers[userIndex] = posPlayer
    console.log(`Player: ${player1}, IndexPos: ${userIndex}, Position: ${posPlayer}`)
  } else if (losingPlayer === player2) {
    posPlayers[userIndex + 1] = posPlayer
    console.log(`Player: ${player2}, IndexPos: ${userIndex + 1}, Position: ${posPlayer}`)
  }
  userIndex += 2;
}

// Function to handle final match position updates
function setFinalPositions(losingPlayer: string): void {
  console.log(`Setting final position for: ${player1Name.value}, Match Index: ${indexGame}`)
  console.log(`Setting final position for: ${player2Name.value}, Match Index: ${indexGame}`)
  const playerOneIndex = props.players.findIndex(
    (
      data // Find the player index
    ) => data.player === player1Name.value
  )
  const playerTwoIndex = props.players.findIndex(
    (
      data // Find the player index
    ) => data.player === player2Name.value
  )

  let pos = (5 - indexGame);

  console.log(`Player Indexes Found: ${playerOneIndex} ${playerTwoIndex}`)
  if (playerOneIndex !== -1 && playerTwoIndex !== -1) {
    if (player1Name.value === losingPlayer) { // Player two won
      posPlayers[playerOneIndex] = pos
      posPlayers[playerTwoIndex] = pos - 1
    }
    else
    { // Player one won
      posPlayers[playerOneIndex] = pos -1
      posPlayers[playerTwoIndex] = pos
    }
    console.log(`Player: ${player1Name.value}, IndexPos: ${playerOneIndex}, Position: ${posPlayers[playerOneIndex]}`)
    console.log(`Player: ${player2Name.value}, IndexPos: ${playerTwoIndex}, Position: ${posPlayers[playerTwoIndex]}`)
  } else {
    console.error(`Player ${player1Name.value} not found in the tournament`)
    console.error(`Player ${player2Name.value} not found in the tournament`)
  }
}

function setFinalNames() {
  player1Name.value = finalOne
  player2Name.value = finalTwo
}

const updatePlayerData = (storeType: string) => {
  const playerOneName = player1Name.value
  const playerTwoName = player2Name.value
  // Find given player inside the players array
  const playerOneIndex = players.findIndex((p) => p.player === playerOneName)
  if (playerOneIndex !== -1) { // Update data for the given player
    const score = numScorePlayerOne
    let len = player_scores[playerOneIndex].length
    // Subtract one from len if it is greater than one
    if (indexGame < 2 || len === 2)
      len = len > 0 ? len - 1 : len
    console.log(len)
    console.log(indexGame)
    if (storeType == IS_STATE) {
      player_scores[playerOneIndex][len] = (score)
    }
    else {
      player_scores[playerOneIndex].pop()
      player_scores[playerOneIndex].push(score)
    }
    player_hits[playerOneIndex] += playerOne.getHits()
  }
  const playerTwoIndex = players.findIndex((p) => p.player == playerTwoName)
  if (playerTwoIndex !== -1) { // Update data for the given player
    const score = numScorePlayerTwo

    let len = player_scores[playerTwoIndex].length
    // Subtract one from len if it is greater than one
    if (indexGame < 2 || len === 2)
      len = len > 0 ? len - 1 : len
    console.log(len)
    if (storeType == IS_STATE) {
      player_scores[playerTwoIndex][len] = (score)
    }
    else {
      player_scores[playerTwoIndex].pop()
      player_scores[playerTwoIndex].push(score)
    }
    player_hits[playerTwoIndex] += playerTwo.getHits()
  }
  playerOne.resetHits()
  playerTwo.resetHits()
}

// Main function to manage the tournament flow
function manageTournament(winPlayer: string, losingPlayer: string, matchIndex: number): void {
  console.log(`Results: {${numScorePlayerOne}} {${numScorePlayerTwo}}`)

  switch (matchIndex) {
    case 1:
      finalOne = winPlayer
      updatePlayerData(IS_COMPLETED)
      setSemiPositions(losingPlayer)
      player1Name.value = player_names[2]
      player2Name.value = player_names[3]
      break
    case 2:
      finalTwo = winPlayer
      updatePlayerData(IS_COMPLETED)
      setSemiPositions(losingPlayer)
      setFinalNames()
      break
    default:
      console.error('Invalid match index')
      break
  }

  playerTwo.setName(player2Name.value)
  playerOne.setName(player1Name.value)
}

function emitData(status: string) {
  setTimeout(() => {
    const tournament_type = playerCount === 4 ? '4P' : '8P'
    // Emit the tournament data to the parent component
    let time_played = Date.now() / 1000 - startTime + stateTime
    time_played = Math.floor(time_played)
    // Emit the tournament data to the parent component
    emit('gameOver', {
      status: status,
      tournament_type: tournament_type,
      time_played: time_played,
      player_ids: ids,
      player_names: player_names,
      player_scores: player_scores,
      player_hits: player_hits,
      players: status === IS_STATE ? [] : players.map((player, index) => ({
        id: player.id,
        name_player: player.player,
        scores: player_scores[index],
        time_played: time_played,
        hits: player_hits[index],
        position: posPlayers[index]
      })),
      final_round: status === IS_STATE ? [] : {
        player_one: finalOne,
        player_two: finalTwo,
        winner: winner,
        loser: loser
      },
    })
  }, 1000)
}

// Index to track the current game in the tournament
let indexGame = 0

const endGame = (winningPlayer: string, losingPlayer: string) => {
  // Remove the ability to start the game for a short period
  window.removeEventListener('keydown', toggleAnimation)
  three.removeScene(luckySphere.get())
  finalScore.updateScore(winningPlayer + ' wins!')
  three.addScene(finalScore.get())
  blinkObject(finalScore.get())
  isAnimating.value = false

  indexGame += 1
  if (indexGame < playerCount - 1) {
    // Tournament is not finished
    manageTournament(winningPlayer, losingPlayer, indexGame)
    setTimeout(() => {
      three.removeScene(finalScore.get())
      window.addEventListener('keydown', toggleAnimation)
      resetScores()
      setHelpText()
    }, 2000)
    // Tournament is finished
  } else if (indexGame === playerCount - 1) {
    updatePlayerData(IS_COMPLETED)
    setFinalPositions(losingPlayer)

    setTimeout(() => {
      finalScore.updateScore('Returning to home...')
    }, 2000)
    winner = winningPlayer
    loser = losingPlayer
    isGameOver.value = true
    emitData(IS_COMPLETED)
  }
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
  playerOne?.dispose()
  playerTwo?.dispose()
  ball.dispose()
  horizWallDown.dispose()
  horizWallUp.dispose()
  wallMid.dispose()
  scorePlayer1.dispose()
  scorePlayer2.dispose()
  helpTextPlayerOne.dispose()
  helpTextPlayerTwo.dispose()
  window.removeEventListener('resize', () => {
    three.resize(window.innerWidth, window.innerHeight)
  })
  window.removeEventListener('keydown', toggleAnimation)
})
</script>

<template>
  <div></div>
</template>
