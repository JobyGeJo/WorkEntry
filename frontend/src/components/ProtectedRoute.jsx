import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import auth from '../auth'

function ProtectedRoute({ children, setUser }) {
    const [loading, setLoading] = useState(true)
    const [authenticated, setAuthenticated] = useState(false)

    useEffect(() => {
        const checkSession = async () => {
            try {
                const res = await auth.get('/session')
                setAuthenticated(true)
                setUser(res.data.data) // store the whole user object
            } catch {
                setAuthenticated(false)
            } finally {
                setLoading(false)
            }
        }
        checkSession()
    }, [setUser])

    if (loading) return <p>Loading...</p>
    return authenticated ? children : <Navigate to="/" />
}

export default ProtectedRoute

