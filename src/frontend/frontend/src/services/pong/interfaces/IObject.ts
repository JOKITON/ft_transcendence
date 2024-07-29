import { Mesh, MeshBasicMaterial, MeshStandardMaterial } from 'three'

export default interface IObject {
  mesh: Mesh
  material: MeshStandardMaterial | MeshBasicMaterial
  get(): Mesh
  moveUp(y: number): void
  moveDown(y: number): void
}
