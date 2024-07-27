import { Scene, PerspectiveCamera, WebGLRenderer, Mesh } from 'three'

export default class ThreeService implements IThreeService {
  private scene: Scene
  private camera: PerspectiveCamera
  private renderer: WebGLRenderer

  constructor(width: number = window.innerWidth, height: number = window.innerHeight) {
    this.scene = new Scene()
    this.camera = new PerspectiveCamera(75, width / height, 0.1, 1000)
    this.renderer = new WebGLRenderer()
    this.renderer.setSize(width, height)
    this.camera.position.z = 10
    document.body.appendChild(this.renderer.domElement)
  }

  addScene(Mesh: Mesh): void {
    this.scene.add(Mesh)
  }

  remove(Mesh: Mesh): void {
    this.scene.remove(Mesh)
  }

  resize(width: number, height: number): void {
    this.camera.aspect = width / height
    this.camera.updateProjectionMatrix()
    this.renderer.setSize(width, height)
  }

  animate(): void {
    const render = (): void => {
      requestAnimationFrame(render)
      this.renderer.render(this.scene, this.camera)
    }
    render()
  }

  removeRenderer(): void {
    document.body.removeChild(this.renderer.domElement)
  }

  destructor(): void {
    this.removeRenderer()
  }
}
