import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ProtectedRoute from './components/ProtectedRoute'
import {useState} from "react";
import './App.css'

function App() {
    const [user, setUser] = useState(null)
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute setUser={setUser}>
                            <Dashboard user={user} />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/"
                    element={
                        <ProtectedRoute setUser={setUser}>
                            <Dashboard user={user} />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    )
}

export default App
