import { Mesh, MeshBasicMaterial, MeshStandardMaterial } from 'three'

export default interface IObject {
  get(): Mesh
}
