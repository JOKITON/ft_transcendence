import type IPlayer from './interfaces/IPlayer';
import Box from './Objects/Box';
import Sphere from './Objects/Sphere';
import { Sphere as ThreeSphere, BoxGeometry, Color, Vector3 } from 'three';

export default class Player extends Box implements IPlayer {
  private name: string = 'NPC';
  private score: number = 0;
  private up: string;
  private down: string;
  private keys: Set<string> = new Set();
  private keydownListener: (event: KeyboardEvent) => void;
  private keyupListener: (event: KeyboardEvent) => void;

  constructor(
    geometry: Vector3,
    color: Color,
    position: Vector3 ,
    up: string,
    down: string
  ) {
    super(geometry, color, position);
    this.down = down;
    this.up = up;
    this.setupEventListeners();
  }

  setName(name: string): void {
    this.name = name;
  }

  getName(): string {
    return this.name;
  }

  addScore(): void {
    this.score += 1;
  }

  getScore(): number {
    return this.score;
  }

  private setupEventListeners(): void {
    this.keydownListener = (event: KeyboardEvent) => {
      this.keys.add(event.key);
    };

    this.keyupListener = (event: KeyboardEvent) => {
      this.keys.delete(event.key);
    };

    window.addEventListener('keydown', this.keydownListener);
    window.addEventListener('keyup', this.keyupListener);
  }

  update(): void {
    if (this.keys.has(this.up) && this.mesh.position.y < 6) {
      this.moveUp(0.4);
    } else if (this.keys.has(this.down) && this.mesh.position.y > -6) {
      this.moveDown(0.4);
    }
  }

  dispose(): void {
    // Dispose of geometry and material
    if (this.mesh.geometry) this.mesh.geometry.dispose();
    if (this.mesh.material) {
      if (this.mesh.material instanceof Array) {
        this.mesh.material.forEach(mat => mat.dispose());
      } else {
        this.mesh.material.dispose();
      }
    }

    // Remove event listeners
    window.removeEventListener('keydown', this.keydownListener);
    window.removeEventListener('keyup', this.keyupListener);
    
    console.log('Player disposed');
  }

  public getBoundingSphere(): ThreeSphere {
    const size = (this.mesh.geometry as BoxGeometry).parameters;
    const radius = Math.sqrt(size.width ** 2 + size.height ** 2 + size.depth ** 2) / 2;
    return new ThreeSphere(this.mesh.position, radius);
  }

  public intersects(other: Sphere): boolean {
    const playerSphere = this.getBoundingSphere();
    const ballSphere = other.getBoundingSphere();
    return playerSphere.intersectsSphere(ballSphere);
  }
}
