<setup setup lang="ts">
export default {
  name: 'Pong'
}
</setup>

<script setup lang="ts">
import { Console } from 'console'
import { X509Certificate } from 'crypto'
import * as THREE from 'three'

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)

const renderer = new THREE.WebGLRenderer()
renderer.setSize(window.innerWidth, window.innerHeight)
renderer.setAnimationLoop(animate)
document.body.appendChild(renderer.domElement)

const geometry = new THREE.SphereGeometry(2, 30, 30)
const material = new THREE.MeshPhongMaterial({ color: 0x00ff00, wireframe: false })
const bola = new THREE.Mesh(geometry, material)
const bola2 = new THREE.Mesh(geometry, material)
scene.add(bola)
scene.add(bola2)
camera.position.z = 5

bola2.position.x = 2
bola2.position.y = 2
bola2.position.z = -1
scene.background = new THREE.Color(0x4)
scene.add(new THREE.AmbientLight(0x404040))

const light = new THREE.DirectionalLight(0xffffff)
light.position.set(2, 1, 1).normalize()
scene.add(light)

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
    }
    // colaider de la escena con el cubo
  })
  renderer.render(scene, camera)
  // vamos a crear un colaider del grande la escene
}
function keys2(cube: THREE.Object3D) {
  const l = 0.01
  window.addEventListener('keydown', (e) => {
    console.log(e.key + '<- key preisionada')
    switch (e.key) {
      case 'w':
        cube.position.y += l
        break
      case 's':
        cube.position.y -= l
        break
    }
    // colaider de la escena con el cubo
  })
  renderer.render(scene, camera)
  // vamos a crear un colaider del grande la escene
}
function animate() {
  keys(bola)
  keys2(bola2)

  requestAnimationFrame(animate)
}
</script>

<template>
  <canvas>
    {{ animate }}
  </canvas>

  <!-- al final puedo llamar objetos del script -->
</template>
<style>
canvas {
  display: block;
  align-items: center;
  justify-content: center;
  margin: auto;
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
}
</style>
