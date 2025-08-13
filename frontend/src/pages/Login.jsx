import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import authServices from "../services/authServices.js";
import "../styles/login.sass"

function Login() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        await authServices.login({ id: parseInt(username), password }).then((response) => {
            if (response.status === 200) {
                navigate('/dashboard');
            } else {
                setError(response.data.message || response.data.error || 'Login failed')
            }
        }).catch((error) => {
            setError(
                error.response?.data?.message ||
                error.response?.data?.error ||
                'An error occurred while logging in'
            )
        })
    }


    return (
        <div className="container login-container">
            <h1>Work Entry</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Login</button>
                {error && <p className="error">{error}</p>}
            </form>
        </div>
    )
}

export default Login
