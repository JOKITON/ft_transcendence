import { Color, Mesh, MeshBasicMaterial, BoxGeometry, Vector3 } from 'three'

import type IObject from '../interfaces/IObject'
import Geometries from 'three/examples/jsm/renderers/common/Geometries.js'

export default class Box implements IObject {
  protected mesh: Mesh
  protected material: MeshBasicMaterial
  protected geometry: BoxGeometry

  constructor(geometry: Vector3, color: Color, position: Vector3) {
    this.geometry = new BoxGeometry(geometry.x, geometry.y, geometry.z)
    this.material = new MeshBasicMaterial({ color })
    this.mesh = new Mesh(this.geometry, this.material)
    this.mesh.position.set(position.x, position.y, position.z)
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
