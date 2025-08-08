// src/services/authService.js
import axios from 'axios'

class AuthService {
    constructor() {
        this.auth = axios.create({
            baseURL: '/auth/v1', // vite.config.js proxy will send to backend
            withCredentials: true // important! send/receive cookies
        })
    }

    async login(payload) {
        return this.auth.post('/login', payload)
    }

    async logout() {
        return this.auth.post('/logout')
    }

    async session() {
        return this.auth.get('/session')
    }

    async register(payload) {
        return this.auth.post('/register', payload)
    }
}

export default new AuthService()
