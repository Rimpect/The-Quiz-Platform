import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import cleanCSS from 'vite-plugin-clean-css'

// https://vite.dev/config/
export default defineConfig({
  build: {
    sourcemap: false,
    cssCodeSplit: true,
  },
  css: {
    devSourcemap: true,
  },
  plugins: [
    react(),
    cleanCSS({
      clean: true, // Удалять CSS файлы после сборки
      sourceMap: false, // Не генерировать source maps
    }),
  ],
})
