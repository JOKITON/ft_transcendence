import type IPlayer from './interfaces/IPlayer';
import Box from './Objects/Box';
import Sphere from './Objects/Sphere';
import { Sphere as ThreeSphere, BoxGeometry, Color, Vector3 } from 'three';

export default class Player extends Box implements IPlayer {
  private name: string = 'NPC';
  private position: Vector3;
  private score: number = 0;
  private up: string;
  private down: string;
  private keys: Set<string> = new Set();

  constructor(
    geometry: Vector3,
    color: Color,
    position: Vector3,
    up: string,
    down: string
  ) {
    super(geometry, color, position);
    this.position = position;
    this.up = up;
    this.down = down;
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
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
  }

  private handleKeyDown = (event: KeyboardEvent): void => {
    if (event.code === this.up) {
      this.keys.add(this.up);
    } else if (event.code === this.down) {
      this.keys.add(this.down);
    }
  }

  private handleKeyUp = (event: KeyboardEvent): void => {
    if (event.code === this.up) {
      this.keys.delete(this.up);
    } else if (event.code === this.down) {
      this.keys.delete(this.down);
    }
  }

  update(): void {
    if (this.keys.has(this.up) && this.mesh.position.y < 6) {
      this.moveUp(0.15);
    } 
    if (this.keys.has(this.down) && this.mesh.position.y > -6) {
      this.moveDown(0.15);
    }
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

    // Remove event listeners
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
    
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

  public returnToPlace() {
    this.mesh.position.x = (this.position.x);
    this.mesh.position.y = (this.position.y);
    this.mesh.position.z = (this.position.z);
  }
}
