import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import authServices from '../services/authService';
import { motion } from 'framer-motion';

export default function Navbar({ user, setUser }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await authServices.logout();
    setUser(null);
    navigate('/login');
  };

  return (
    <nav className="bg-primary/80 backdrop-blur-lg border-b border-border sticky top-0 z-50">
      <div className="container mx-auto px-6 py-3 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-text-primary">
          Work<span className="text-accent">Entry</span>
        </Link>
        <div className="flex items-center space-x-6">
          {user ? (
            <>
              <Link to="/profile" className="text-text-secondary hover:text-accent font-medium transition-colors">Profile</Link>
              <Link to="/dashboard" className="text-text-secondary hover:text-accent font-medium transition-colors">Dashboard</Link>
              {user.role === 'Admin' && (
                <Link to="/admin" className="text-text-secondary hover:text-accent font-medium transition-colors">Admin Panel</Link>
              )}
              <button onClick={handleLogout} className="text-text-secondary hover:text-accent font-medium transition-colors">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-text-secondary hover:text-accent font-medium transition-colors">Login</Link>
              <Link to="/register" className="bg-accent text-white px-4 py-2 rounded-md font-semibold hover:bg-blue-700 transition-colors">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}