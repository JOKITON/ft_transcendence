import { defineConfig } from 'vite'
import path from "path"
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import tsconfigPaths from 'vite-tsconfig-paths'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx(), vueDevTools(), tsconfigPaths()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "assets": path.resolve(__dirname, "./src/assets"),
      "pong": path.resolve(__dirname, './src/services/pong'),
      "pong-utils": path.resolve(__dirname, './src/services/pong/Objects/Utils'),
      "pong-objects": path.resolve(__dirname, './src/services/pong/Objects')
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
        // Add other entry points if needed
      }
    }
  },
  server: {
    host: '0.0.0.0',
    port: 80,
    open: true,
    cors: true
  }
})
