import type Player from '../Player'

export default interface IKeyboard {
  keys: Set<string>
  player: Player
  addKey(key: string): void
}
