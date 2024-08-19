import { Color, Mesh, MeshPhongMaterial, Vector3 } from 'three';
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';

const depth = 0.15,
  size = 2;

export default class Score {
  private mesh: Mesh;
  private material: MeshPhongMaterial;
  private font?: Font;
  private textGeometry?: TextGeometry;

  constructor(score: string, color: Color, initialPos: Vector3) {
    this.material = new MeshPhongMaterial({ color });
    this.mesh = new Mesh(); // Initialize mesh without geometry
    this.mesh.position.set(initialPos.x, initialPos.y, initialPos.z);

    // Load font asynchronously
    this.loadFont().then(() => {
      this.updateScore(score); // Update text after font is loaded
    });
  }

  private async loadFont() {
    return new Promise<void>((resolve, reject) => {
      const loader = new FontLoader();
      loader.load(
        './src/assets/fonts/Bit5x3_Regular.json', // Font URL
        (font) => {
          this.font = font;
          resolve();
        },
        undefined,
        (error) => {
          console.error('An error occurred while loading the font:', error);
          reject(error);
        }
      );
    });
  }

  private updateText(score: string) {
    if (!this.font) return;

    // Dispose old geometry if it exists
    if (this.textGeometry) {
      this.textGeometry.dispose();
    }

    this.textGeometry = new TextGeometry(score, {
      font: this.font,
      size: size,
      depth: depth,
      curveSegments: 0,
      bevelThickness: 0.15,
      bevelSize: 0,
      bevelEnabled: true
    });
      // Compute bounding box
    this.textGeometry.computeBoundingBox(); 
    const boundingBox = this.textGeometry.boundingBox;

    if (boundingBox) {
      // Calculate center offset
      const offsetX = -(boundingBox.max.x + boundingBox.min.x) / 2;
      const offsetY = -(boundingBox.max.y + boundingBox.min.y) / 2;

      // Apply translation to center the text
      this.textGeometry.translate(offsetX, offsetY, 0);
    }

    // Update mesh with new geometry
    this.mesh.geometry = this.textGeometry;
    this.mesh.material = this.material;
  }

  public updateScore(endingText: string) {
    this.updateText(endingText);
  }

  public get(): Mesh {
    return this.mesh;
  }

  public update() {

  }

  dispose(): void {
    // Dispose of geometry and material
    if (this.mesh.geometry) this.mesh.geometry.dispose();
    if (this.mesh.material) {
      if (Array.isArray(this.mesh.material)) {
        this.mesh.material.forEach(mat => mat.dispose());
      } else {
        this.mesh.material.dispose();
      }
    }
    
    console.log('Score disposed');
  }
}
