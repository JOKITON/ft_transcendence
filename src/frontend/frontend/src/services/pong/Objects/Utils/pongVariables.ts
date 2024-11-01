import { Vector3 } from 'three'

export interface intStatePongData {
  check: boolean
  id: number
  status: string
  tournament_type: string
  player_ids: Array<number>
  player_names: Array<string>
  player_scores: Array<number>
  player_hits: Array<number>
  time_played: number
  // aiDifficulty: number,
  // isAudioEnabled: boolean,
}

export interface intStateTournamentPongData {
  check: boolean
  id: number
  status: string
  tournament_type: string
  player_ids: Array<number>
  player_names: Array<string>
  player_scores: Array<Array<number>>
  player_hits: Array<number>
  time_played: number
  game_index: number
  // aiDifficulty: number,
  // isAudioEnabled: boolean,
}

export const dateStart = Date.now() / 1000

// Define bounds of the Pong game
export const bounds = { minX: -16.2, maxX: 16.2, minY: -9.2, maxY: 9.2, minZ: 0, maxZ: 0 }

// Ball and walls
export const ballVectorY = Math.random() * 0.2 - 0.1

let ballVelocityX = -0.25
export let ballVelocity = new Vector3(ballVelocityX, ballVectorY, 0)

export function setBallVelocity(aiDiff: number) {
  switch (aiDiff) {
    case 0.3:
      ballVelocityX = -0.15
      break
    case 0.5:
      ballVelocityX = -0.2
      break
    case 1:
      ballVelocityX = -0.25
      break
    case 1.5:
      ballVelocityX = -0.3
      break
    default:
      ballVelocityX = -0.25
      break
  }
  console.log('AI Speed: ', ballVelocityX)
  ballVelocity = new Vector3(ballVelocityX, ballVectorY, 0)
}

export const ballGeometry = [0.33, 10, 10]

export const ballGeometry2 = [0.66, 10, 10]

export const vecHorizWall = new Vector3(33, 0.3, 1)

export const SCORE_TO_WIN = 3
export const IS_STATE = 'P'
export const IS_COMPLETED = 'C'
export const BIT_FONT = 'fonts/Bit5x3_Regular.json'
export const MONTSERRAT_FONT = 'fonts/Montserrat.json'

import FontService from 'pong-objects/Text/FontService';
import { Font } from 'three/examples/jsm/loaders/FontLoader'
const { loadFont } = FontService;
export let font : Font | null = null
loadFont(BIT_FONT).then((loadedFont) => {
  font = loadedFont
})