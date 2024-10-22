import Player from '../Player'
import Sphere from '../Sphere'

function checkCollisions(ball: Sphere, player: Player, player2: Player): boolean {
  const playerIntersects = ball.intersects(player) || ball.intersects(player2)

  if (playerIntersects) {
    ball.invertVelocity() // Reverse ball direction upon collision
    ball.randomizeDirection()
    return true
  }
  return false
}

export function handleCollisions(ball: Sphere, player: Player, player2: Player): void {
  // Check for collisions every 10ms
  const collisionDetected = checkCollisions(ball, player, player2)

  if (collisionDetected) {
    ball.speedUp(0.025)

    // Play collision sound
    const audio = new Audio('/src/assets/songs/ball-hit.mp3')
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
