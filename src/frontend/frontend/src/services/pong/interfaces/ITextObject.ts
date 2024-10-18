import { Color, Mesh, MeshPhongMaterial, Vector3 } from 'three';
import { Font } from 'three/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';

export default interface ITextObject {
	name: string
	mesh: Mesh
	material: MeshPhongMaterial
	font?: Font
	textGeometry?: TextGeometry

	constructor(score: string, color: Color, initialPos: Vector3) : void
	loadFont() : Promise<void>
	updateText(score: string): void
	updateScore(numScore: number) : void
	get(): Mesh
	dispose(): void
}
