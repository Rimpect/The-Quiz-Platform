import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  build: {
    sourcemap: false,
    cssCodeSplit: true,
  },
  css: {
    devSourcemap: true,
  },
  plugins: [react()],
})
