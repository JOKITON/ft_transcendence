import { Color, Mesh, MeshPhongMaterial, Vector3 } from 'three'
import { Font, FontLoader } from 'three/examples/jsm/loaders/FontLoader.js'
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js'
import type ITextObject from '../../interfaces/ITextObject'

const depth = 0.15,
  size = 2

export default class DashedWall implements ITextObject {
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
    this.updateScore(score) // Update text after font is loaded
  }

  private updateText(score: string): void {
    if (!this.font) return

    // Dispose old geometry if it exists
    if (this.textGeometry) {
      this.textGeometry.dispose()
    }

    this.textGeometry = new TextGeometry(score, {
      font: this.font,
      size: size,
      depth: depth,
      curveSegments: 0,
      bevelThickness: 0.15,
      bevelSize: 0,
      bevelEnabled: true
    })
    // Compute bounding box
    this.textGeometry.computeBoundingBox()
    const boundingBox = this.textGeometry.boundingBox

    if (boundingBox) {
      // Calculate center offset
      const offsetX = -(boundingBox.max.x + boundingBox.min.x) / 2
      const offsetY = -(boundingBox.max.y + boundingBox.min.y) / 2

      // Apply translation to center the text
      this.textGeometry.translate(offsetX, offsetY, 0)
    }

    // Update mesh with new geometry
    this.mesh.geometry = this.textGeometry
    this.mesh.material = this.material

    this.mesh.rotation.z = Math.PI / 2 // Rotate 90 degrees around X-axis
  }

  public updateScore(numScore: string) : void {
    const num = parseInt(numScore)
    if (num > 99 || num < -99) this.updateText('0')
    else this.updateText(numScore)
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
