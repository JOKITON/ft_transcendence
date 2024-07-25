import type Box from '../Objects/Box'

export default interface Iplayer {
  name: string
  score: number
  _up: string
  _down: string

  setName(name: string): void
  getName(): string
  addScore(): void
  getScore(): number
  event(): void
}
