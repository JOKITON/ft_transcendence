import { Color, Mesh, MeshBasicMaterial, SphereGeometry, Vector3, Sphere as ThreeSphere } from 'three';
import Player from './../Player'

export default class Sphere {
  protected mesh: Mesh;
  protected material: MeshBasicMaterial;
  protected geometry: SphereGeometry;
  protected velocity: Vector3;

  // Define the game area boundaries
  private readonly minX: number;
  private readonly maxX: number;
  private readonly minY: number;
  private readonly maxY: number;
  private readonly minZ: number;
  private readonly maxZ: number;

  constructor(
    vector: Vector3,
    color: Color,
    initialPos: Vector3,
    velocity: Vector3,
    bounds: { minX: number, maxX: number, minY: number, maxY: number, minZ: number, maxZ: number }
  ) {
    this.geometry = new SphereGeometry(vector.x, vector.y, vector.z);
    this.material = new MeshBasicMaterial({ color });
    this.mesh = new Mesh(this.geometry, this.material);
    this.mesh.position.set(initialPos.x, initialPos.y, initialPos.z);
    this.velocity = velocity;

    // Set boundaries for the game area
    this.minX = bounds.minX;
    this.maxX = bounds.maxX;
    this.minY = bounds.minY;
    this.maxY = bounds.maxY;
    this.minZ = bounds.minZ;
    this.maxZ = bounds.maxZ;
  }

  get(): Mesh {
    return this.mesh;
  }

  update(): number {
    // Update position based on velocity
    this.mesh.position.add(this.velocity);

    // Check for collisions with boundaries and reverse velocity if needed
    return (this.checkCollisions());
  }

  private checkCollisions(): number {
    // Check collisions with the X boundaries
    if (this.mesh.position.x <= this.minX) {
      this.velocity.x *= -1;
      return 1;
    } else if (this.mesh.position.x >= this.maxX) {
      this.velocity.x *= -1;
      return 2;
    }

    // Check collisions with the Y boundaries
    if (this.mesh.position.y <= this.minY) {
      this.velocity.y *= -1;
    } else if (this.mesh.position.y >= this.maxY) {
      this.velocity.y *= -1;
    }

    // Check collisions with the Z boundaries (if applicable)
    if (this.mesh.position.z <= this.minZ) {
      this.mesh.position.z = this.minZ;
      this.velocity.z *= -1;
    } else if (this.mesh.position.z >= this.maxZ) {
      this.mesh.position.z = this.maxZ;
      this.velocity.z *= -1;
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

  public invertVelocity(velocity: number) {
    this.velocity.x *= velocity;
  }

  public goMiddle() {
    this.mesh.position.x = 0
    this.mesh.position.y = 0
    this.mesh.position.z = 0
  }
}
