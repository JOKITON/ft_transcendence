// FontService.ts
import { FontLoader, Font } from 'three/examples/jsm/loaders/FontLoader.js'

class FontService {
  // Font is declared as a static property, so it is shared among all instances of the class
  private static font: Font | null = null

  public static async loadFont(url: string): Promise<Font> {
    return new Promise((resolve, reject) => {
      const loader = new FontLoader()
      loader.load(
        url,
        (font) => {
          FontService.font = font
          resolve(font)
        },
        undefined,
        (error) => {
          console.error('An error occurred while loading the font:', error)
          reject(error)
        }
      )
    })
  }

  static getFont(): Font | null {
    return this.font
  }
}

export default FontService
