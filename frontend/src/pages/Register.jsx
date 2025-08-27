import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import authServices from '../services/authService';

export default function Register() {
  const [formData, setFormData] = useState({
    full_name: '',
    username: '',
    password: '',
    phone_number: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); setSuccess('');
    try {
      await authServices.register(formData);
      setSuccess('Registration successful! Please log in.');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed.');
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
        <h1 className="text-3xl font-bold text-center text-text-primary mb-2">Create Your Account</h1>
        <p className="text-center text-text-secondary mb-6">Join your team and start tracking your work.</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input name="full_name" placeholder="Full Name" onChange={handleChange} required className="w-full px-4 py-3 border border-border rounded-md" />
          <input name="username" placeholder="Username (no spaces or numbers)" onChange={handleChange} required className="w-full px-4 py-3 border border-border rounded-md" />
          <input name="password" type="password" placeholder="Password (min 8 chars, 1 number, 1 symbol)" onChange={handleChange} required className="w-full px-4 py-3 border border-border rounded-md" />
          <input name="phone_number" placeholder="Phone Number (optional)" onChange={handleChange} className="w-full px-4 py-3 border border-border rounded-md" />
          <button type="submit" className="w-full py-3 bg-accent text-white font-semibold rounded-md hover:bg-blue-700">
            Sign Up
          </button>
          {error && <p className="text-red-500 text-center">{error}</p>}
          {success && <p className="text-green-500 text-center">{success}</p>}
        </form>
        <p className="text-center text-text-secondary text-sm mt-6">
          Already have an account? <Link to="/login" className="text-accent font-semibold hover:underline">Sign In</Link>
        </p>
      </motion.div>
    </div>
  );
}