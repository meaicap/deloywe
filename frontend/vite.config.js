import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/auth': 'http://127.0.0.1:8000',
      '/upload': 'http://127.0.0.1:8000',
      '/flashcard': 'http://127.0.0.1:8000',
      '/quiz': 'http://127.0.0.1:8000',
      '/documents': 'http://127.0.0.1:8000',
    }
  },
  // Ensure build works for production
  build: {
    outDir: 'dist',
  }
})
