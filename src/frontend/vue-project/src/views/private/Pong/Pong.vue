<setup setup lang="ts">
  export default {
    name: 'Pong'
  }
  </setup>
  
  <script setup lang="ts">
  import { Vector3, Color } from 'three'
  import ThreeServices from '../../../services/pong/ThreeService'
  import Player from '../../../services/pong/Player'
  import Sphere from '../../../services/pong/Objects/Sphere'
  import DashedWall from '../../../services/pong/Objects/DashedWall'

  const three = new ThreeServices(1400, 600)

  const sphere = new Sphere()

  const horizWallUp = new Player(new Vector3(33, 0.2, 0.2), new Color(), new Vector3(0, 7, 0))
  const horizWallDown = new Player(new Vector3(33, 0.2, 0.2), new Color(), new Vector3(0, -7, 0))
  const points = [new Vector3(0.05, -7, 0.05), new Vector3(0.05, 7, 0.05)];
  const vertWallMid = new DashedWall(points, new Color('white'), 0.5, 0.5);
  
  const player = new Player()
  const player2 = new Player(new Vector3(0.2, 2, 0.2), new Color(), new Vector3(-16, 0, 0), 'w', 's')
  
  sphere.position(new Vector3(0, 0, 0))
  
  // Walls & Vertical dashed lines
  three.addScene(horizWallUp.get())
  three.addScene(horizWallDown.get())
  three.addScene(vertWallMid.get())
  
  // Players
  three.addScene(player.get())
  three.addScene(player2.get())
  
  // Ball
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
  