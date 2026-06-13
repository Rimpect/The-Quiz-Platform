import path from 'path'

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  base: '/The-Quiz-Platform/',
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
  plugins: [react()],
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
})
