import { IPong } from './IPong'
import * as THREE from 'three'
/*
export class Pong implements IPong {
  config(): void {
    import * as THREE from 'three'
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    )
  }
}*/

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)

const renderer = new THREE.WebGLRenderer()
renderer.setSize(window.innerWidth, window.innerHeight)
renderer.setAnimationLoop(animate)
document.body.appendChild(renderer.domElement)

const geometry = new THREE.SphereGeometry(1, 32, 32)
const material = new THREE.MeshPhongMaterial({ color: 0x00ff00, wireframe: false })
const bola = new THREE.Mesh(geometry, material)
scene.add(bola)

camera.position.z = 5

scene.background = new THREE.Color(0x4)

scene.add(new THREE.AmbientLight(0x404040))

const light = new THREE.DirectionalLight(0xffffff)

light.position.set(1, 1, 1).normalize()
scene.add(light)

// y que se pueda controlar con las teclas
//
//
function keys(cube: THREE.Object3D) {
  const l = 0.01
  window.addEventListener('keydown', (e) => {
    switch (e.key) {
      case 'ArrowUp':
        cube.position.y += l
        break
      case 'ArrowDown':
        cube.position.y -= l
        break
      case 'ArrowLeft':
        cube.position.x -= l
        break
      case 'ArrowRight':
        cube.position.x += l
        break
    }
    // colaider de la escena con el cubo
  })
  // vamos a crear un colaider del grande la escene
}
function animate(): void {
  keys(bola)
  keys(camera)
  camera.lookAt(scene.position)

  renderer.render(scene, camera)
  //THREE.Box3().setFromObject(cube)
}
