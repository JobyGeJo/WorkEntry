import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    // https: {
    //   key: fs.readFileSync(path.resolve(__dirname, 'cert/192.168.1.20-key.pem')),
    //   cert: fs.readFileSync(path.resolve(__dirname, 'cert/192.168.1.20.pem'))
    // },
    proxy: {
      '/auth': 'http://localhost:8000',
      '/api': 'http://localhost:8000'
    }
  }
})
