import { Color, Mesh, MeshBasicMaterial, BoxGeometry, Vector3 } from 'three'

export default class Box {
  protected mesh: Mesh
  protected material: MeshBasicMaterial
  protected geometry: BoxGeometry
  protected up: string
  protected down: string

  constructor(geometry: Vector3, color: Color, position: Vector3, up: string, down: string) {
    this.geometry = new BoxGeometry(geometry.x, geometry.y, geometry.z)
    this.material = new MeshBasicMaterial({ color })
    this.mesh = new Mesh(this.geometry, this.material)
    this.mesh.position.set(position.x, position.y, position.z)
    if (up && down) {
      this.up = up
      this.down = down
    }
  }

  get(): Mesh {
    return this.mesh
  }

  moveUp(y: number): void {
    this.mesh.position.y += y
  }

  moveDown(y: number): void {
    this.mesh.position.y -= y
  }
}
