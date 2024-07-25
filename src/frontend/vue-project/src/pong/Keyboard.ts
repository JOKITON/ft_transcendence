import type IKeyboard from './interfaces/IKeyboard'

export default class Keyboard implements IKeyboard {
  keys: Set<string>

  constructor() {
    this.keys = new Set<string>()
  }
}
