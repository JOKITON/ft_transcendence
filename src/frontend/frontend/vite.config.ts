import { defineConfig } from 'vite'
import path from "path"
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx(), vueDevTools()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api/v1/auth/': {
        target: 'http://auth:80',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/auth/, '/api/auth'),
      },
      '/api/v1/pong/': {
        target: 'http://pong:80',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/pong/, '/api/pong'),
      },
      '/api/v1/friendship/': {
        target: 'http://friendship:80',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/admin/, '/api/admin'),
      },
      '/api/v1/livechat/ws/': {
        target: 'http://livechat:80',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/admin/, '/api/admin'),
      },
    },
    open: true,
    cors: true
  }
})
