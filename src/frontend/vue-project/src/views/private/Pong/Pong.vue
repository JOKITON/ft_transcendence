<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'
import { Vector3, Color } from 'three'
import ThreeService from '../../../services/pong/ThreeService'
import Player from '../../../services/pong/Player'
import Sphere from '../../../services/pong/Objects/Sphere'
import DashedWall from '../../../services/pong/Objects/DashedWall'
import { randInt } from 'three/src/math/MathUtils.js'

const three = new ThreeService(window.innerWidth, window.innerHeight)

const bounds = { minX: -16.2, maxX: 16.2, minY: -6.2, maxY: 6.2, minZ: 0, maxZ: 0 }
const ballVectorY = randInt(-0.1, 0.1);
const ball = new Sphere(new Vector3(0.33, 10, 10), new Color(0x00f9ed), new Vector3(0, 0, 0), new Vector3(0.15, ballVectorY, 0), bounds)

const horizWallUp = new Player(new Vector3(33, 0.2, 0), new Color(), new Vector3(0, 7, 0))
const horizWallDown = new Player(new Vector3(33, 0.2, 0), new Color(), new Vector3(0, -7, 0))

const points = [new Vector3(0.05, -7, 0.05), new Vector3(0.05, 7, 0.05)]
const vertWallMid = new DashedWall(points, new Color('white'), 0.33, 0.5)

const player = new Player(new Vector3(0.4, 2, 0.5), new Color(), new Vector3(16, 0, 0), 'ArrowUp', 'ArrowDown')
const player2 = new Player(new Vector3(0.4, 2, 0.5), new Color(), new Vector3(-16, 0, 0), 'w', 's')

function setupScene() {
  three.addScene(horizWallUp.get())
  three.addScene(horizWallDown.get())
  three.addScene(vertWallMid.get())
  three.addScene(player.get())
  three.addScene(player2.get())
  three.addScene(ball.get())
}

// Time control for collision detection
let collisionCheckInterval = 10; // in milliseconds
let lastCollisionCheckTime = 0;
let collisionAmounts = 0;

function handleCollisions() {
  const now = performance.now();
  if (now - lastCollisionCheckTime >= collisionCheckInterval) {
    const collisionDetected = checkCollisions();
    
    if (collisionDetected) {
      collisionAmounts++;
      // Increase interval if collisions are frequent
      if (collisionAmounts) {
        collisionCheckInterval = 200;
        if (collisionAmounts > 5)
          ball.goMiddle();
      }
    } else {
      // Reset count and interval if no collisions
      collisionAmounts = 0;
      if (collisionCheckInterval !== 10) {
        collisionCheckInterval = 10;
      }
    }

    lastCollisionCheckTime = now;
  }
}

let playerOneLost = 1;
let playerTwoLost = 2;

function update() {
  let check = ball.update();
  if (check) {
    if ( check == playerOneLost )
      console.log('Player 1 lost!');
    else if ( check == playerTwoLost )
      console.log('Player 2 lost!');
    else
      console.log('Wrong value for losing...');
    return ;
  }
  player.update();
  player2.update();

  handleCollisions();
}

function checkCollisions(): boolean {
  const playerIntersects = ball.intersects(player) || ball.intersects(player2);

  if (playerIntersects) {
    ball.invertVelocity(-1); // Reverse ball direction upon collision
    return true;
  }
  return false;
}

onMounted(() => {
  setupScene()
  three.startAnimation(update)
  window.addEventListener('resize', () => {
    three.resize(window.innerWidth, window.innerHeight)
  })
})

onBeforeUnmount(() => {
  three.stopAnimation()
  three.dispose()
})
</script>

<template>
  <div></div> <!-- No canvas in the template; the renderer is handled by ThreeService -->
</template>
