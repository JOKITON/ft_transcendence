import type IKeyboard from './interfaces/IKeyboard'

export default class Keyboard implements IKeyboard {
  keys: Set<string>
  objetct: number

  constructor(typePlayer: string) {
    this.keys = new Set()
    this.objetct = this.choosePlayer(typePlayer)
  }

  choosePlayer(type: string): number {
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

  controlPlayer(): void {
    console.log('controlPlayer')
  }
  //
  addKey(key: string): void {
    //addEventListener('keydown', (event): void => {})
    //addEventListener('keyup', (event): void => {})
    //this.keys.add(key)
  }
}
