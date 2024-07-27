import type IPongGame from './interfaces/IPongGame'
import Player from './Player'
import TreeService from './ThreeService'

export default class PongGame implements IPongGame {
  private treeService: TreeService = new TreeService(800, 600)
  private player1: Player = new Player()
  private player2: Player = new Player()

  constructor() {}
  start(): void {}
  update(): void {}
  destructor(): void {}
  animate(): void {}
}
