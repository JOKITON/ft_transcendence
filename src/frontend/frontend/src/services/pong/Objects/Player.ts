import type IPlayer from '../interfaces/IPlayer';
import Box from './Box';
import Sphere from './Sphere';
import { Sphere as ThreeSphere, BoxGeometry, Color, Vector3 } from 'three';

export default class Player extends Box implements IPlayer {
  private orGeometry: Vector3;
  private orColor: Color;
  private orPosition: Vector3;

  private hits : number = 0;

  private name: string = 'NPC';
  private position: Vector3;
  private score: number = 0;
  private moveSpeed: number = 0.35;

  private aiDifficulty: number = 1;
  private reactionDelay: number = 300;
  private isAI: boolean = false;

  private up: string;
  private down: string;
  private keys: Set<string> = new Set();

  private oldBallPosX: number = 0;
  private oldBallPosY: number = 0;

  constructor(
    geometry: Vector3,
    color: Color,
    position: Vector3,
    up: string,
    down: string,
    name: string,
  ) {
    super(geometry, color, position);
    
    this.orGeometry = geometry;
    this.orColor = color;
    this.orPosition = position;

    this.position = position;
    this.name = name;
    if (up && down) {
      this.up = up;
      this.down = down;
      this.setupEventListeners();
    }
    else {
      this.isAI = true;
    }
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
    event.preventDefault();
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

  setAiDifficulty(difficulty: number): void {
    this.aiDifficulty = difficulty;
    this.reactionDelay = (300 / this.aiDifficulty); // Adjust this value to make the AI slower
    // console.log(this.reactionDelay);
  }

  updateAI(ball: Sphere): void {
    if (this.isAI)
      this.manageAI(ball);
  }

  update(): void {
    if (this.keys.has(this.up) && this.mesh.position.y < 8) {
      this.moveUp(0.35);
    }
    if (this.keys.has(this.down) && this.mesh.position.y > -8) {
      this.moveDown(0.35);
    }
  }

  public setSpeed(speed: number): void {
    this.moveSpeed = speed;
  }

  manageAI(ball: Sphere): void {
    const ballPos = ball.get();
    const ballPosX = ballPos.position.x;
    const ballPosY = ballPos.position.y;
    
    setTimeout(() => {
      if (ball.get().position.x != 0) {
        const velocityX = ballPosX - this.oldBallPosX;
        const velocityY = ballPosY - this.oldBallPosY;

        let randomFactor = 0;
        if (this.aiDifficulty < 10)
          randomFactor = ((Math.random() * 0.05) * (0.01 / this.aiDifficulty)); // Adjust the randomness factor
        // Assuming 'this.mesh.position.x' is the AI's paddle position on the X-axis
        const timeToImpact = (this.mesh.position.x - ballPosX) / velocityX; // Time it takes for the ball to reach the AI paddle's X position

        // Predict Y position when the ball reaches the AI
        const predictedBallPosY = (ballPosY + (velocityY * timeToImpact)) * (1);
        if (this.mesh.position.y < predictedBallPosY && (this.mesh.position.y < 8)) {
          this.moveUp(this.moveSpeed - randomFactor);
        } else if (this.mesh.position.y > predictedBallPosY && (this.mesh.position.y > -8)) {
          this.moveDown(this.moveSpeed - randomFactor);
        }
      }

      this.oldBallPosX = ballPosX;
      this.oldBallPosY = ballPosY;

    }, this.reactionDelay);
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
    if (!this.isAI) {
      window.removeEventListener('keydown', this.handleKeyDown);
      window.removeEventListener('keyup', this.handleKeyUp);
    }
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

  public resize(size: number): void {
    this.mesh.scale.set(size, size, size);
  }

  public addHit() {
    this.hits += 1;
  }

  public getHits() : number {
    const ret : number = this.hits;
    this.hits = 0;
    return ret;
  }

  public returnToPlace() {
    this.mesh.position.x = (this.position.x);
    this.mesh.position.y = (this.position.y);
    this.mesh.position.z = (this.position.z);
    
    this.mesh.scale.set(1, 1, 1);
  }
}
