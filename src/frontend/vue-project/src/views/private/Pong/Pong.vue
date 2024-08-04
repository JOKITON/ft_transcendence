<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { Vector3, Color } from 'three'
import ThreeService from '../../../services/pong/ThreeService'
import Player from '../../../services/pong/Player'
import Sphere from '../../../services/pong/Objects/Sphere'
import DashedWall from '../../../services/pong/Objects/DashedWall'
import Score from '../../../services/pong/Objects/Score'
import { randInt } from 'three/src/math/MathUtils.js'
import { handleCollisions } from '../../../services/pong/Utils'

const three = new ThreeService(window.innerWidth, window.innerHeight)

const bounds = { minX: -16.2, maxX: 16.2, minY: -6.2, maxY: 6.2, minZ: 0, maxZ: 0 }
const ballVectorY = randInt(-100, 100) / 1000;
const ball = new Sphere(new Vector3(0.33, 10, 10), new Color(0x00f9ed), new Vector3(0, 0, 0), new Vector3(0.15, ballVectorY, 0), bounds)

const horizWallUp = new Player(new Vector3(33, 0.2, 0), new Color(), new Vector3(0, 7, 0))
const horizWallDown = new Player(new Vector3(33, 0.2, 0), new Color(), new Vector3(0, -7, 0))

const points = [new Vector3(0.05, -7, 0.05), new Vector3(0.05, 7, 0.05)]
const vertWallMid = new DashedWall(points, new Color('white'), 0.33, 0.5)

const player = new Player(new Vector3(0.4, 2, 0.5), new Color(), new Vector3(16, 0, 0), 'ArrowUp', 'ArrowDown')
const player2 = new Player(new Vector3(0.4, 2, 0.5), new Color(), new Vector3(-16, 0, 0), 'w', 's')

// const scorePlayer1 = new Score('0', new Color('black'), new Vector3(0, 0, 0));

function setupScene() {
  three.addScene(horizWallUp.get())
  three.addScene(horizWallDown.get())
  three.addScene(vertWallMid.get())
  three.addScene(player.get())
  three.addScene(player2.get())
  three.addScene(ball.get())
  // three.addScene(scorePlayer1.get())
}

let playerOneLost = 1;
let playerTwoLost = 2;
const isAnimating = ref(true);

function update() {
  if (!isAnimating.value) return;
  let check = ball.update();
  if (check) {
    if ( check == playerOneLost )
      console.log('Player 1 lost!');
    else if ( check == playerTwoLost )
      console.log('Player 2 lost!');
    else
      console.log('Wrong value for losing...');
    isAnimating.value = false;
    return ;
  }
  player.update();
  player2.update();

  handleCollisions(ball, player, player2);
}

function toggleAnimation(event: KeyboardEvent) {
  if (event.code === 'Space') {
    isAnimating.value = !isAnimating.value; // Toggle the animation state
    console.log(`Animation ${isAnimating.value ? 'resumed' : 'paused'}`);
  }
}

onMounted(() => {
  setupScene()
  three.startAnimation(update)
  window.addEventListener('resize', () => {
    three.resize(window.innerWidth, window.innerHeight)
  })
  window.addEventListener('keydown', toggleAnimation)
})

onBeforeUnmount(() => {
  three.stopAnimation()
  three.dispose()
  window.addEventListener('keydown', toggleAnimation)
})
</script>

<template>
  <div></div> <!-- No canvas in the template; the renderer is handled by ThreeService -->
</template>
