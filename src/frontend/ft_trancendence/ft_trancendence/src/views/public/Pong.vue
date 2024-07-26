<setup setup lang="ts">
export default {
  name: 'Pong'
}
</setup>

<script setup lang="ts">
import { Vector3, Color } from 'three'
import ThreeServices from '../../services/pong/ThreeService'
import Player from '../../services/pong/Player'
import Sphere from '../../services/pong/Objects/Sphere'

const three = new ThreeServices(1400, 600)

const sphere = new Sphere()

const muroHorizontal = new Player(new Vector3(33, 0.2, 0.2), new Color(), new Vector3(0, 7, 0))
const muroVertical = new Player(new Vector3(33, 0.2, 0.2), new Color(), new Vector3(0, -7, 0))
const vertical = new Player(new Vector3(0.1, 13, 0.2), new Color(), new Vector3(0, 0, 0))

const player = new Player()
const player2 = new Player(new Vector3(0.2, 2, 0.2), new Color(), new Vector3(-16, 0, 0), 'w', 's')

sphere.position(new Vector3(0, 0, 0))

// muros de la cancha
three.addScene(muroHorizontal.get())
three.addScene(vertical.get())
three.addScene(muroVertical.get())

// jugadores
three.addScene(player.get())
three.addScene(player2.get())

// pelota
three.addScene(sphere.get())

function animate() {
  requestAnimationFrame(animate)
  player.update()
  player2.update()
  three.animate()
}

animate()
</script>

<template>
  <canvas> {{ animate() }}</canvas>
</template>
