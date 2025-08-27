import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import authServices from "../services/authService"; // <-- IMPORT IT HERE

function ProtectedRoute({ children, setUser, adminOnly = false }) {
    const [loading, setLoading] = useState(true);
    const [authenticatedUser, setAuthenticatedUser] = useState(null);

    useEffect(() => {
        const checkSession = async () => {
            try {
                // USE IT HERE to check the session
                const res = await authServices.session();
                const userData = res.data.data;
                
                // Assign a role based on the backend data
                userData.role = userData.account?.role || "Employee";
                
                setAuthenticatedUser(userData);
                setUser(userData);
            } catch {
                setAuthenticatedUser(null);
            } finally {
                setLoading(false);
            }
        };
        checkSession();
    }, [setUser]);

    if (loading) return <div className="text-center p-10">Loading...</div>;

    if (!authenticatedUser) {
        return <Navigate to="/login" />;
    }

    if (adminOnly && authenticatedUser.role !== 'Admin') {
        return <Navigate to="/dashboard" />;
    }

    return children;
}

export default ProtectedRoute;