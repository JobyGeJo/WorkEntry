import axios from 'axios';

const auth = axios.create({
    baseURL: '/auth/v1',
    withCredentials: true
});

class AuthService {
    login(payload) { return auth.post('/login', payload); }
    logout() { return auth.post('/logout'); }
    session() { return auth.get('/session'); }
    register(payload) { return auth.post('/register', payload); }
}

export default new AuthService();