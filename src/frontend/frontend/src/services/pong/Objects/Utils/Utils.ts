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
