import type Iplayer from './interfaces/IPlayer'
import Box from './Objects/Box'
import { Color, Vector3 } from 'three'

export default class Player extends Box implements Iplayer {
  private score: number = 0
  private name: string = 'NPC'
  private keys: Set<string>

  constructor(
    geometry: Vector3 = new Vector3(),
    color: Color = new Color(),
    position: Vector3 = new Vector3(0.2, 2, 0.2)
  ) {
    super(geometry, color, position) // esto se refiere a la clase padre
    //  this.event()
  }

  setName(name: string): void {
    this.name = name
  }

  getName(): string {
    return this.name
  }

  setScore(score: number): void {
    this.score = score
  }

  getScore(): number {
    return this.score
  }

  event(): void {}

  destructor(): void {
    console.log('destructor Player')
  }
}
