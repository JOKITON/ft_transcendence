<setup setup lang="ts">
export default {
  name: 'Pong'
}
</setup>

<script setup lang="ts">
import { Vector3, Color } from 'three'
import ThreeServices from '../../services/pong/Three'
import Player from '../../services/pong/Player'
import Sphere from '../../services/pong/Objects/Sphere'

const three = new ThreeServices(1400, 800)

const sphere = new Sphere()
const player = new Player()

const player2 = new Player(
  new Vector3(0.5, 2, 0.5),
  new Color(0x00ff00),
  new Vector3(6, 0, 0),
  'w',
  's'
)
sphere.position(new Vector3(0, 0, 0))

three.addScene(player.get())
three.addScene(player2.get())

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
