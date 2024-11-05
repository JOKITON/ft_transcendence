import { Color, Mesh, MeshPhongMaterial, Vector3 } from 'three'
import { Font, FontLoader } from 'three/examples/jsm/loaders/FontLoader.js'
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js'

const depth = 0.15,
  size = 2

export default class DashedWall {
  private mesh: Mesh
  private material: MeshPhongMaterial
  private font?: Font
  private textGeometry?: TextGeometry

  constructor(score: string, color: Color, initialPos: Vector3, font: Font) {
    this.material = new MeshPhongMaterial({ color })
    this.mesh = new Mesh() // Initialize mesh without geometry
    this.mesh.position.set(initialPos.x, initialPos.y, initialPos.z)

    // Load font asynchronously
    this.font = font
  }

  public get(): Mesh {
    return this.mesh
  }

  public update() {}

  dispose(): void {
    // Dispose of geometry and material
    if (this.mesh.geometry) this.mesh.geometry.dispose()
    if (this.mesh.material) {
      if (Array.isArray(this.mesh.material)) {
        this.mesh.material.forEach((mat) => mat.dispose())
      } else {
        this.mesh.material.dispose()
      }
    }
  }
}
