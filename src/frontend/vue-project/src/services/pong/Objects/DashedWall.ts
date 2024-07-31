import { Color, LineSegments, LineDashedMaterial, BufferGeometry, Float32BufferAttribute, Vector3 } from 'three';
import type IObject from '../interfaces/IObject';

export default class DashedLine implements IObject {
  protected line: LineSegments;
  protected material: LineDashedMaterial;
  protected geometry: BufferGeometry;

  constructor(
    points: Vector3[] = [new Vector3(0.2, -1, 0.2), new Vector3(0.2, 1, 0.2)],
    color: Color = new Color(0xffffff),
    dashSize: number = 1,
    gapSize: number = 0.5
  ) {
    this.geometry = new BufferGeometry().setFromPoints(points);
    
    this.material = new LineDashedMaterial({
      color: color,
      dashSize: dashSize,
      gapSize: gapSize,
      linewidth: 2 // Line width (optional)
    });

    this.line = new LineSegments(this.geometry, this.material);
    this.line.computeLineDistances(); // Required for dashed lines
  }

  get(): LineSegments {
    return this.line;
  }

  moveUp(y: number): void {
    this.line.position.y += y;
  }

  moveDown(y: number): void {
    this.line.position.y -= y;
  }

  position(vector: Vector3): void {
    this.line.position.set(vector.x, vector.y, vector.z);
  }

  setPoints(points: Vector3[]): void {
    this.geometry.setFromPoints(points);
    this.line.computeLineDistances(); // Recompute line distances for updated points
  }

  /* update(): void {
    // You can implement any animation or updates here if needed
  } */
}
