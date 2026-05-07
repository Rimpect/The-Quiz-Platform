import path from 'path'

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  base: '/The-Quiz-Platform/',
  build: {
    sourcemap: false,
    cssCodeSplit: true,
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
