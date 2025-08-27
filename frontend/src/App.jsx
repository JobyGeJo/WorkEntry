import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Pages and Components
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import UserProfile from './pages/UserProfile'; // <-- IMPORT THE NEW COMPONENT

function App() {
    const [user, setUser] = useState(null);

    return (
        <Router>
            <Routes>
                <Route element={<Layout user={user} setUser={setUser} />}>
                    {/* Public Routes */}
                    <Route path="/" element={<LandingPage />} />
                    
                    {/* Auth Routes */}
                    <Route path="/login" element={<Login setUser={setUser} />} />
                    <Route path="/register" element={<Register />} />

                    {/* Protected Employee Route */}
                    <Route
                        path="/dashboard"
                        element={
                            <ProtectedRoute setUser={setUser}>
                                <Dashboard user={user} />
                            </ProtectedRoute>
                        }
                    />

                     {/* Protected Admin Route */}
                    <Route
                        path="/admin"
                        element={
                            <ProtectedRoute setUser={setUser} adminOnly={true}>
                                <AdminDashboard />
                            </ProtectedRoute>
                        }
                    />
                    
                    {/* ADDED: Protected User Profile Route */}
                    <Route
                        path="/profile"
                        element={
                            <ProtectedRoute setUser={setUser}>
                                <UserProfile user={user} />
                            </ProtectedRoute>
                        }
                    />
                    
                    {/* Redirect any other path to the landing page */}
                    <Route path="*" element={<Navigate to="/" />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;