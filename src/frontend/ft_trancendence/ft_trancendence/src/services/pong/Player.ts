import type Iplayer from './interfaces/IPlayer'
import Box from './Objects/Box'
import { Color, Vector3, Vector2 } from 'three'
import Keyboard from './Keyboard'

export default class Player extends Box implements Iplayer {
  private score: number = 0
  private name: string = 'NPC'
  private up: string
  private down: string
  private keys: { [key: string]: boolean } = {}
  //private keyboard: Keyboard = new Keyboard() <- no se si implemenratala o no pero para controlador online y demas igual y si

  constructor(
    geometry: Vector3 = new Vector3(0.2, 2, 0.2),
    color: Color = new Color(),
    position: Vector3 = new Vector3(-8, 0.2, 0.2),
    up: string = 'ArrowUp',
    down: string = 'ArrowDown'
  ) {
    super(geometry, color, position) // esto se refiere a la clase padre
    this.down = down
    this.up = up
    this.event()
  }

  setName(name: string): void {
    this.name = name
  }

  getName(): string {
    return this.name
  }

  addScore(): void {
    this.score += 1
  }

  getScore(): number {
    return this.score
  }

  event(): void {
    addEventListener('keydown', (event): void => {
      this.keys[event.key] = true
    })

    addEventListener('keyup', (event): void => {
      this.keys[event.key] = false
    })
  }

  update(): void {
    if (this.keys[this.up]) {
      this.moveUp(0.2)
    } else if (this.keys[this.down]) {
      this.moveDown(0.2)
    }
  }

  destructor(): void {
    console.log('destructor Player')
  }
}
