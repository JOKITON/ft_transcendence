import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx(), vueDevTools()],
  server: {
    host: '0.0.0.0',
    port: 80,
    proxy: {
      '/api/csrf/': {
        target: 'http://csrf:8000', // Updated to match backend port
        changeOrigin: true,
      },
      '/api/auth/': {
        target: 'http://auth:8000', // Updated to match backend port
        changeOrigin: true,
      },
      '/api/pong/': {
        target: 'http://pong:8000', // Updated to match backend port
        changeOrigin: true,
      },
      '/api/user/': {
        target: 'http://pong:8000', // Updated to match backend port
        changeOrigin: true,
      }
    },
    open: true,
    cors: true
  }
})
