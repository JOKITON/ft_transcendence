import { Color, Mesh, MeshPhongMaterial, Vector3 } from 'three';
import { Font } from 'three/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';

export default interface ITextObject {
	name: string
	mesh: Mesh
	material: MeshPhongMaterial
	font?: Font
	textGeometry?: TextGeometry
	size: number

	constructor(score: string, color: Color, initialPos: Vector3, fontType: string, size: number) : void
	loadFont(fontType: string) : Promise<void>
	updateText(score: string): void
	updateScore(numScore: number) : void
	get(): Mesh
	dispose(): void
}
