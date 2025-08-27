import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/apiService';
import { motion } from 'framer-motion';
import { FiUsers, FiFileText } from 'react-icons/fi';

export default function AdminDashboard() {
const [users, setUsers] = useState([]);
const [selectedUser, setSelectedUser] = useState(null);
const navigate = useNavigate();

useEffect(() => {
    const fetchUsers = async () => {
        const response = await apiService.getAllUsers();
        setUsers(response.data.data || []);
    };
    fetchUsers();
}, []);

return (
    <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold text-text-primary mb-6">Administrator Dashboard</h1>
        <div className="grid md:grid-cols-12 gap-6 items-start">
            <motion.div 
                className="md:col-span-4 bg-primary border border-border p-6 rounded-lg shadow-sm"
                initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }}>
                <h2 className="text-xl font-bold mb-4 text-text-primary flex items-center space-x-2">
                    <FiUsers /><span>Employees</span>
                </h2>
                <ul className="space-y-2 max-h-[60vh] overflow-y-auto">
                    {users.map(user => (
                        <li key={user.user_id} onClick={() => setSelectedUser(user)}
                            className={`p-3 rounded-md cursor-pointer font-medium transition-colors ${selectedUser?.user_id === user.user_id ? 'bg-accent text-white' : 'hover:bg-secondary text-text-secondary'}`}>
                            {user.full_name}
                        </li>
                    ))}
                </ul>
            </motion.div>

            <motion.div 
                className="md:col-span-8 bg-primary border border-border rounded-lg shadow-sm p-8 text-center"
                initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }}>
                <FiFileText className="text-5xl text-gray-300 mx-auto mb-4" />
                {selectedUser ? (
                    <div>
                        <h2 className="text-2xl font-bold text-text-primary">{selectedUser.full_name}</h2>
                        <p className="text-text-secondary mb-6">Select an action for this user.</p>
                        <button 
                            onClick={() => navigate(`/work-logs/${selectedUser.user_id}`)}
                            className="bg-accent text-white font-semibold px-6 py-3 rounded-md flex items-center justify-center space-x-2 mx-auto"
                        >
                            <span>View Work Log History</span>
                        </button>
                    </div>
                ) : (
                    <p className="text-text-secondary mt-4">Please select an employee from the list to view their details.</p>
                )}
            </motion.div>
        </div>
    </div>
);
}