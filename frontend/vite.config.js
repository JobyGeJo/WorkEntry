import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Proxy API requests to FastAPI backend
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 443,
    https: {
      key: fs.readFileSync(path.resolve(__dirname, 'cert/192.168.1.20-key.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, 'cert/192.168.1.20.pem'))
    },
    proxy: {
      '/auth': 'http://localhost:8000'
    }
  }
})
