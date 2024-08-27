import type Player from '../Player'

export default interface IKeyboard {
  choosePlayer(type: string): number
}
