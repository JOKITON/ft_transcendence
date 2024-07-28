import { Mesh, MeshBasicMaterial, MeshStandardMaterial, Vector3 } from 'three'

export default interface IObject {
  mesh: Mesh
  material: MeshStandardMaterial | MeshBasicMaterial
  get(): Mesh
  up(y: number): void
  down(y: number): void
  update(): void
}
