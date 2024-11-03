import type Player from '../Objects/Player'

export default interface IKeyboard {
  keys: Set<string>
  player: Player
  choosePlayer(type: string): number
  controlPlayer(): void
}
