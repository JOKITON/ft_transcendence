<script>
import * as THREE from 'three'

export default {
  name: 'PongGame',
  mounted() {
    this.initThreeJS()
  },
  methods: {
    initThreeJS() {
      // Escena
      const scene = new THREE.Scene()

      // Cámara
      const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      )
      camera.position.z = 5

      // Renderizador
      const renderer = new THREE.WebGLRenderer()
      renderer.setSize(window.innerWidth, window.innerHeight)
      this.$refs.pongGame.appendChild(renderer.domElement)

      // Crear objetos (paletas y bola)
      const paddleGeometry = new THREE.BoxGeometry(1, 0.1, 0.1)
      const paddleMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff })

      const paddle1 = new THREE.Mesh(paddleGeometry, paddleMaterial)
      paddle1.position.set(0, -3, 0)
      scene.add(paddle1)

      const paddle2 = new THREE.Mesh(paddleGeometry, paddleMaterial)
      paddle2.position.set(0, 3, 0)
      scene.add(paddle2)

      const ballGeometry = new THREE.SphereGeometry(0.1, 32, 32)
      const ballMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff })

      const ball = new THREE.Mesh(ballGeometry, ballMaterial)
      scene.add(ball)

      // Animación
      const animate = () => {
        requestAnimationFrame(animate)
        renderer.render(scene, camera)
      }

      animate()
    }
  }
}
</script>

<template>
  <div ref="pongGame"></div>
</template>

<style scoped>
div {
  width: 100%;
  height: 100%;
}
</style>
