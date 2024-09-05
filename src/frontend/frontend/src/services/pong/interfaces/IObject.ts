import { Mesh, MeshBasicMaterial, MeshStandardMaterial } from 'three'

export default interface IObject {
  mesh: Mesh
  material: MeshStandardMaterial | MeshBasicMaterial
  get(): Mesh
}
