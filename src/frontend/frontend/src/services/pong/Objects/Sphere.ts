import { Color, Mesh, MeshBasicMaterial, SphereGeometry, Vector3, Sphere as ThreeSphere } from 'three';
import Player from './Player'

export default class Sphere {
  protected mesh: Mesh;
  protected material: MeshBasicMaterial;
  protected geometry: SphereGeometry;
  protected velocity: Vector3;
  protected inVelocity: number;

  // Define the game area boundaries
  private readonly minX: number;
  private readonly maxX: number;
  private readonly minY: number;
  private readonly maxY: number;
  private readonly minZ: number;
  private readonly maxZ: number;

  constructor(
    vector: Array<number>,
    color: Color,
    initialPos: Vector3,
    velocity: Vector3,
    bounds: { minX: number, maxX: number, minY: number, maxY: number, minZ: number, maxZ: number }
  ) {
    this.geometry = new SphereGeometry(vector[0], vector[1], vector[2]);
    this.material = new MeshBasicMaterial({ color });
    this.mesh = new Mesh(this.geometry, this.material);
    this.mesh.position.set(initialPos.x, initialPos.y, initialPos.z);
    this.velocity = velocity;
    this.inVelocity = velocity.x;

    // Set boundaries for the game area
    this.minX = bounds.minX;
    this.maxX = bounds.maxX;
    this.minY = bounds.minY;
    this.maxY = bounds.maxY;
    this.minZ = bounds.minZ;
    this.maxZ = bounds.maxZ;
  }

  public get(): Mesh {
    return this.mesh;
  }

  public getVelocity(): boolean {
    return (this.velocity.x > 0);
  }

  update(): number {
    // Update position based on velocity
    this.mesh.position.add(this.velocity);

    // Check for collisions with boundaries and reverse velocity if needed
    return (this.checkCollisions());
  }

  public setVelocityX(velocityX: number): void {
    if (velocityX)
      this.velocity.x = velocityX;
  }
  public setVelocityY(velocityY: number): void {
    if (velocityY)
      this.velocity.y = velocityY;
  }
  public setVelocityZ(velocityZ: number): void {
    if (velocityZ)
      this.velocity.z = velocityZ;
  }

  private checkCollisions(): number {
    // Check collisions with the X boundaries
    if (this.mesh.position.x < this.minX) {
      this.velocity.x = this.inVelocity;
      this.velocity.x *= -1;
      this.setPosition(new Vector3(0, 0, 0));
      return 1;
    } else if (this.mesh.position.x > this.maxX) {
      this.velocity.x = this.inVelocity;
      this.velocity.x *= -1;
      this.setPosition(new Vector3(0, 0, 0));
      return 2;
    }

    // Check collisions with the Y boundaries
    if (this.mesh.position.y <= this.minY) {
      this.velocity.y *= -1;
    } else if (this.mesh.position.y >= this.maxY) {
      this.velocity.y *= -1;
    }

    return 0;
  }

  // Create a bounding sphere for collision detection
  public getBoundingSphere(): ThreeSphere {
    // Assume the sphere radius is the same as its geometry's radius
    const radius = (this.geometry as SphereGeometry).parameters.radius;
    return new ThreeSphere(this.mesh.position, radius);
  }

  // Check if this sphere intersects with another sphere
  public intersects(other: Player): boolean {
    const thisSphere = this.getBoundingSphere();
    const otherSphere = other.getBoundingSphere();
    return thisSphere.intersectsSphere(otherSphere);
  }

  public invertVelocity(): void {
    this.velocity.x *= -1;
  }

  public randomizeDirection(): void {
    const randNum = Math.random();
    if (randNum > 0.5)
      this.velocity.y -= (randNum * 0.1);
    else  
      this.velocity.y += (randNum * 0.1);
  }

  public setPosition(pos: Vector3) {
    this.mesh.position.x = pos.x;
    this.mesh.position.y = pos.y;
    this.mesh.position.z = pos.z;
  }

  public speedUp(speed: number) {
    if (Math.abs(this.velocity.x) > 1)
      return ;
    if (this.velocity.x < 0)
      this.velocity.x -= speed;
    else
      this.velocity.x += speed;
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
  }
}
