import Player from './Player'
import Sphere from './Objects/Sphere'

// Time control for collision detection
let collisionCheckInterval = 10; // in milliseconds
let lastCollisionCheckTime = 0;
let collisionAmounts = 0;

function checkCollisions(ball : Sphere, player : Player, player2 : Player): boolean {
	const playerIntersects = ball.intersects(player) || ball.intersects(player2);
  
	if (playerIntersects) {
	  ball.invertVelocity(-1); // Reverse ball direction upon collision
	  return true;
	}
	return false;
}

export function handleCollisions(ball : Sphere, player: Player, player2 : Player) {
  const now = performance.now();
  if (now - lastCollisionCheckTime >= collisionCheckInterval) {
    const collisionDetected = checkCollisions(ball, player, player2);
    
    if (collisionDetected) {
	  ball.speedUp(0.025);
      collisionAmounts++;
      // Increase interval if collisions are frequent
      collisionCheckInterval = 100;
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
