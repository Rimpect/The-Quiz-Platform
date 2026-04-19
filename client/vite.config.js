import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  base: '/The-Quiz-Platform/',
  build: {
    sourcemap: false,
    cssCodeSplit: true,
  },
  plugins: [react()],
})
