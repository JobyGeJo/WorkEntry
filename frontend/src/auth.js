import axios from 'axios'

const auth = axios.create({
    baseURL: '/auth/v1', // vite.config.js proxy will send to backend
    withCredentials: true // important! send/receive cookies
})

export default auth
