import { Object3D, Scene, PerspectiveCamera, WebGLRenderer, Mesh } from 'three';
import { AmbientLight, DirectionalLight } from 'three';

const ambientLight = new AmbientLight(0xffffff, 0.5); // Ambient light with a low intensity
const directionalLight = new DirectionalLight(0xffffff, 1); // Directional light with a high intensity
directionalLight.position.set(10, 10, 10).normalize();

export default class ThreeService {
  private scene: Scene;
  private camera: PerspectiveCamera;
  private renderer: WebGLRenderer;
  private animationFrameId: number | null = null;

  constructor(width: number = window.innerWidth, height: number = window.innerHeight) {
    this.scene = new Scene();
    this.camera = new PerspectiveCamera(100, width / height, 0.01, 1000); // Adjusted FOV for better view
    this.renderer = new WebGLRenderer({ antialias: false });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.camera.position.z = 10;

    // Append renderer canvas to the DOM
    document.body.appendChild(this.renderer.domElement);
  }

  addScene(object: Object3D): void {
    this.scene.add(object);
    this.scene.add(ambientLight);
    this.scene.add(directionalLight);
  }

  removeScene(mesh: Mesh): void {
    // Check if the scene contains the mesh
    if (this.scene.children.includes(mesh)) {
      this.scene.remove(mesh);
    }
  
    // Dispose of the mesh's geometry and material
    if (mesh.geometry) {
      mesh.geometry.dispose();
    }
  
    if (mesh.material) {
      if (Array.isArray(mesh.material)) {
        mesh.material.forEach(mat => mat.dispose());
      } else {
        mesh.material.dispose();
      }
    }
  }
  

  resize(width: number, height: number): void {
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  startAnimation(updateCallback: () => void): void {
    const render = (): void => {
      updateCallback();
      this.renderer.render(this.scene, this.camera);
      this.animationFrameId = requestAnimationFrame(render);
    };

    // Start animation loop
    this.animationFrameId = requestAnimationFrame(render);
  }

  stopAnimation(): void {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  dispose(): void {
    try {
      if (this.scene) {
        this.scene.children.forEach(child => {
          if (child instanceof Mesh) {
            this.removeScene(child);
          }
        });
      }
    } catch (error) {
      console.error('Error disposing scene objects:', error);
    }
  
    try {
      if (this.renderer) {
        this.renderer.dispose();
        if (this.renderer.domElement) {
          document.body.removeChild(this.renderer.domElement);
        }
      }
    } catch (error) {
      console.error('Error disposing renderer:', error);
    }
  }
  
  
  
}
