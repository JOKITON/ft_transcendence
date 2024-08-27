import Box from './Objects/Box'
import { Color, Vector3 } from 'three'

export default class Wall extends Box {
  constructor(geometry: Vector3, position: Vector3, color: Color) {
    super(geometry, color, position)
  }

  public dispose(): void {
    // Dispose of geometry and material
    if (this.mesh.geometry) this.mesh.geometry.dispose()
    if (this.mesh.material) {
      if (Array.isArray(this.mesh.material)) {
        this.mesh.material.forEach((mat) => mat.dispose())
      } else {
        this.mesh.material.dispose()
      }
    }

    console.log('Wall disposed')
  }
}
