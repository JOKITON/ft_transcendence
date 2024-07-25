<setup setup lang="ts">
export default {
  name: 'Pong'
}
</setup>

<script setup lang="ts">
import ThreeServices from '../../../utils/Pong/Three'
import Player from '../../../utils/Pong/Player'
import Sphere from '../../../utils/Pong/Objects/Sphere'
import { Vector3 } from 'three'

const three = new ThreeServices(1400, 800)

const sphere = new Sphere()
const play = new Player()
sphere.position(new Vector3(0, 0, 0))

three.addScene(play.get())

three.addScene(sphere.get())

function animate() {
  requestAnimationFrame(animate)
  three.animate()
  play.update()
  sphere.update()
  play.event()
}

animate()
</script>

<template>
  <canvas> {{ animate }}</canvas>
</template>
