import fs from 'fs'
import path from 'path'

import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

// GitHub Pages не умеет SPA-fallback: копируем index.html в 404.html,
// чтобы прямые переходы по роутам работали. Только для демо-сборки.
const spaFallback404 = () => ({
  name: 'spa-fallback-404',
  closeBundle() {
    const dir = path.resolve(__dirname, 'dist')
    const index = path.join(dir, 'index.html')
    const notFound = path.join(dir, '404.html')
    if (fs.existsSync(index)) {
      fs.copyFileSync(index, notFound)
    }
  },
})

export default defineConfig(({ command, mode }) => {
  // Переменные из .env.* и из окружения (process.env приоритетнее — для CI).
  const env = { ...loadEnv(mode, process.cwd(), ''), ...process.env }
  const isDemo = env.VITE_DEMO === 'true'

  return {
    base: command === 'build' ? env.VITE_BASE || '/' : '/',
    build: {
      sourcemap: false,
      cssCodeSplit: true,
    },
    server: {
      host: true, // слушать 0.0.0.0 — доступно для туннеля/локальной сети
      allowedHosts: true, // принимать запросы с любого хоста (devtunnels.ms и т.п.)
      proxy: {
        // Запросы фронта на /api проксируются на локальный бэкенд.
        // Со второго устройства всё идёт с одного origin — CORS не нужен.
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          ws: true, // проксировать WebSocket (/api/game/ws/...)
        },
      },
    },
    plugins: [react(), ...(isDemo ? [spaFallback404()] : [])],
    resolve: {
      alias: {
        '@widgets': path.resolve(__dirname, 'src/widgets'),
        '@entities': path.resolve(__dirname, 'src/entities'),
        '@features': path.resolve(__dirname, 'src/features'),
        '@shared': path.resolve(__dirname, 'src/shared'),
        '@pages': path.resolve(__dirname, 'src/pages'),
        '@app': path.resolve(__dirname, 'src/app'),
        '@MockData': path.resolve(__dirname, 'src/MockData'),
      },
    },
  }
})
