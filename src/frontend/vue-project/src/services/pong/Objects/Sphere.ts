import { Color, Mesh, MeshBasicMaterial, SphereGeometry, Vector3 } from 'three';

export default class Sphere {
  protected mesh: Mesh;
  protected material: MeshBasicMaterial;
  protected geometry: SphereGeometry;
  protected velocity: Vector3;
  protected initialPos: Vector3;

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

  update(): void {
    // Update velocity based on acceleration
    // this.velocity.add(this.acceleration);

    // Update position based on velocity
    this.mesh.position.add(this.velocity);

    // Check for collisions with boundaries and reverse velocity if needed
    this.checkCollisions();
  }

  private checkCollisions(): void {
    // Check collisions with the X boundaries
    // console.log(this.mesh.position.x);
    if (this.mesh.position.x <= this.minX) {
      this.mesh.position.x = this.minX;
      this.velocity.x *= -1;
    } else if (this.mesh.position.x >= this.maxX) {
      this.mesh.position.x = this.maxX;
      this.velocity.x *= -1;
    }

    // Check collisions with the Y boundaries
    if (this.mesh.position.y <= this.minY) {
      this.mesh.position.y = this.minY;
      this.velocity.y *= -1;
    } else if (this.mesh.position.y >= this.maxY) {
      this.mesh.position.y = this.maxY;
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
  }
}
