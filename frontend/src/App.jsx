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
import UserProfile from './pages/UserProfile';
import WorkLogDetail from './pages/WorkLogDetail';
import WorkLogsPage from './pages/WorkLogspage'; // <-- FIX: Add the missing import here

function App() {
    const [user, setUser] = useState(null);

    return (
        <Router>
            <Routes>
                <Route element={<Layout user={user} setUser={setUser} />}>
                    {/* Public Routes */}
                    <Route path="/" element={<LandingPage user={user} />} />
                    
                    {/* Auth Routes */}
                    <Route path="/login" element={<Login setUser={setUser} />} />
                    <Route path="/register" element={<Register />} />

                    {/* Protected Routes */}
                    <Route path="/dashboard" element={<ProtectedRoute setUser={setUser}><Dashboard user={user} /></ProtectedRoute>} />
                    <Route path="/admin" element={<ProtectedRoute setUser={setUser} adminOnly={true}><AdminDashboard /></ProtectedRoute>} />
                    <Route path="/profile" element={<ProtectedRoute setUser={setUser}><UserProfile user={user} setUser={setUser} /></ProtectedRoute>} />
                    <Route path="/worklog/:timesheetId" element={<ProtectedRoute setUser={setUser}><WorkLogDetail /></ProtectedRoute>} />
                    <Route path="/my-work-logs" element={<ProtectedRoute setUser={setUser}><WorkLogsPage /></ProtectedRoute>} />
                    <Route path="/work-logs/:userId" element={<ProtectedRoute setUser={setUser} adminOnly={true}><WorkLogsPage /></ProtectedRoute>} />

                    {/* Fallback Route */}
                    <Route path="*" element={<Navigate to="/" />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;