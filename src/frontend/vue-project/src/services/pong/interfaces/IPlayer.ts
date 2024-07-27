import type Box from '../Objects/Box'

export default interface Iplayer extends Box {
  score: number
  name: string

  setName(name: string): void
  getName(): string
  setScore(score: number): void
  getScore(): number
  event(): void
}
