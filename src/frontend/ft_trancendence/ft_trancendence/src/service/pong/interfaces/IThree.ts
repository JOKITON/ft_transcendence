import { Scene, PerspectiveCamera, WebGLRenderer, Object3D, Mesh } from 'three'

export default interface IThree {
  //#region Properties
  scene: Scene
  camera: PerspectiveCamera
  renderer: WebGLRenderer
  //#endregion
  //#region Methods
  addScene(Mesh: Mesh): void
  remove(Mesh: Mesh): void
  resize(width: number, height: number): void
  render(): void
  //#endregion
}
