import { Mesh, Audio } from 'three'
import Player from '../Player'
import Sphere from '../Sphere'

let lastCollisionCheck = 0;
let lastCollisionCheck2 = 0;

function checkCollisions(ball: Sphere, player: Player, player2: Player): boolean {
  let playerIntersects = false;
  
  if (ball.intersects(player)) {
    const now = Date.now()
    if (now - lastCollisionCheck < 200) {
      return false
    }
    lastCollisionCheck = now
    playerIntersects = true;
  }
  else if (ball.intersects(player2))
  {
    const now = Date.now()
    if (now - lastCollisionCheck2 < 200) {
      return false
    }
    lastCollisionCheck2 = now
    playerIntersects = true;
  }

  if (playerIntersects) {
    ball.invertVelocity() // Reverse ball direction upon collision
    ball.randomizeDirection()
    return true
  }
  return false
}

export function handleCollisions(ball: Sphere, player: Player, player2: Player, audio: HTMLAudioElement): void {
  // Check for collisions every 10ms
  const collisionDetected = checkCollisions(ball, player, player2)

  if (collisionDetected) {
    ball.speedUp(0.025)

    // Play collision sound
    audio.play()
  }
}

// Blinking effect for the score when a player loses
export function blinkObject(mesh: Mesh) {
  let visible = true
  const blinkDuration = 800
  const blinkInterval = 200

  const intervalId = setInterval(() => {
    visible = !visible
    mesh.visible = visible

    setTimeout(() => {
      clearInterval(intervalId)
      mesh.visible = true
    }, blinkDuration)
  }, blinkInterval)
}
