import { Color, LineSegments, LineDashedMaterial, BufferGeometry, Vector3 } from 'three';

export default class DashedLine {
  protected line: LineSegments;
  protected material: LineDashedMaterial;
  protected geometry: BufferGeometry;

  constructor(
    points: Vector3[],
    color: Color = new Color(0xffffff),
    lineDashedParams: Array<number>,
  ) {
    this.geometry = new BufferGeometry().setFromPoints(points);
    
    this.material = new LineDashedMaterial({
      color: color,
      linewidth: lineDashedParams[0], // Line width (optional)
      dashSize: lineDashedParams[1],
      gapSize: lineDashedParams[2],
    });

    this.line = new LineSegments(this.geometry, this.material);
    this.line.computeLineDistances(); // Required for dashed lines
  }

  get(): LineSegments {
    return this.line;
  }

  position(vector: Vector3): void {
    this.line.position.set(vector.x, vector.y, vector.z);
  }

  setPoints(points: Vector3[]): void {
    this.geometry.setFromPoints(points);
    this.line.computeLineDistances(); // Recompute line distances for updated points
  }

  dispose(): void {
    // Dispose of geometry and material
    if (this.geometry) this.geometry.dispose();
    if (this.material) {
      if (Array.isArray(this.material)) {
        this.material.forEach(mat => mat.dispose());
      } else {
        this.material.dispose();
      }
    }
  }
}
