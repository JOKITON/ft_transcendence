import { Color, Mesh, MeshBasicMaterial, SphereGeometry, Vector3 } from 'three'

import type IObject from '../interfaces/IObject'

export default class Sphere implements IObject {
  mesh: Mesh
  material: MeshBasicMaterial
  private geometry: SphereGeometry

  constructor(vector: Vector3 = new Vector3(0.2, 100, 100), color: Color = new Color(0xff0000)) {
    this.geometry = new SphereGeometry(vector.x, vector.y, vector.z)
    this.material = new MeshBasicMaterial({ color })
    this.mesh = new Mesh(this.geometry, this.material)
  }

  get(): Mesh {
    return this.mesh
  }

  position(vector: Vector3): void {
    this.mesh.position.set(vector.x, vector.y, vector.z)
  }

  update(): void {
    this.mesh.rotation.x += 0.04
    this.mesh.rotation.y += 0.06
  }
}
