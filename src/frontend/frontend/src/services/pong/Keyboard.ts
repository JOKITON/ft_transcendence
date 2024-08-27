import type IKeyboard from './interfaces/IKeyboard'
import Player from './Player'

export default class Keyboard implements IKeyboard {
  keys: Set<string> = new Set()
  player: Player

  constructor(Player: Player) {
    this.player = Player
  }

  public choosePlayer(type: string): number {
    switch (type) {
      case 'online':
      case 'player1': {
        addEventListener('keydown', (event): void => {
          this.keys.add(event.key)
        })
        return 1
      }
      case 'player2': {
        // keys s y w ;

        addEventListener('keydown', (event): void => {
          this.keys.add(event.key)
        })
        return 2
      }
      default:
        return 0
    }
  }

  public controlPlayer(): void {
    console.log('controlPlayer')
  }
}
