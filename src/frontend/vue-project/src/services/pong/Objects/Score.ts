import { Color, Mesh, MeshPhongMaterial, Vector3 } from 'three';
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';

const depth = 0,
  size = 1;

export default class Score {
  private mesh: Mesh;
  private material: MeshPhongMaterial;
  private font?: font;
  private textGeometry?: TextGeometry;

  constructor(score: string, color: Color, initialPos: Vector3) {
    this.material = new MeshPhongMaterial({ color });
    this.mesh = new Mesh(); // Initialize mesh without geometry
    this.mesh.position.set(initialPos.x, initialPos.y, initialPos.z);

    // Load font asynchronously
    this.loadFont().then(() => {
      this.updateText(score); // Update text after font is loaded
    });
  }

  private async loadFont() {
    return new Promise<void>((resolve, reject) => {
      const loader = new FontLoader();
      loader.load(
        './fonts/Roboto.json', // Font URL
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
    });

    // Update mesh with new geometry
    this.mesh.geometry = this.textGeometry;
    this.mesh.material = this.material;
  }

  public updateScore(score: number) {
    this.updateText(score.toString());
  }

  public get(): Mesh {
    return this.mesh;
  }

  public update() {

  }
}
