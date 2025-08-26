import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import authServices from "../services/authService";

function Login({ setUser }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await authServices.login({ username, password });
            if (response.status === 200) {
                const userData = response.data.data;
                userData.role = userData.account?.role || 'Employee';
                setUser(userData);
                navigate('/dashboard');
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Login failed.');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-secondary p-4">
            <motion.div
                className="max-w-md w-full bg-primary p-8 rounded-lg shadow-md border border-border"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", stiffness: 300, damping: 25 }}
            >
                <h1 className="text-3xl font-bold text-center text-text-primary mb-2">Welcome Back</h1>
                <p className="text-center text-text-secondary mb-6">Please enter your details to sign in.</p>
                <form onSubmit={handleSubmit} className="space-y-5">
                    <input
                        className="w-full px-4 py-3 border border-border text-text-primary rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
                        type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required
                    />
                    <input
                        className="w-full px-4 py-3 border border-border text-text-primary rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
                        type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required
                    />
                    <button type="submit" className="w-full py-3 px-4 bg-accent text-white font-semibold rounded-md shadow-sm hover:bg-blue-700">
                        Sign In
                    </button>
                    {error && <p className="text-red-500 text-center font-medium">{error}</p>}
                </form>
                <p className="text-center text-text-secondary text-sm mt-6">
                    Don't have an account? <Link to="/register" className="text-accent font-semibold hover:underline">Sign Up</Link>
                </p>
            </motion.div>
        </div>
    );
}

export default Login;