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
      '/api/v1': {
        target: 'http://auth:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/auth/, '/api/auth'),
      },
      '/api/pong/': {
        target: 'http://pong:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/pong/, '/api/pong'),
      },
      '/api/user/': {
        target: 'http://api:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/user/, '/api/user'),
      },
      '/api/v1/friendship': {
        target: 'http://friendship:80',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/admin/, '/api/admin'),
      },
    },
    open: true,
    cors: true
  }
})
