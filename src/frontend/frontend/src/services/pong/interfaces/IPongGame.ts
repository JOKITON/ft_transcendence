import type Player from '../Player'
import type TreeService from '../ThreeService'

export default interface IPongGame {
  treeService: TreeService
  player1: Player
  player2: Player
  start(): void
  update(): void
  destructor(): void
}
