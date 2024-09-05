export default interface Iplayer {
  name: string
  score: number
  up: string
  down: string
  keys: Set<string>

  setName(name: string): void
  getName(): string
  addScore(): void
  getScore(): number
  event(): void
}
