export default function Dashboard({ user }) {
    return <h1>Welcome, {user?.username || 'Guest'}!</h1>
}
