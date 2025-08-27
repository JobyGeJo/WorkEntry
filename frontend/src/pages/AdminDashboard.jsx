import React, { useState, useEffect } from 'react';
import apiService from '../services/apiService';
import { motion } from 'framer-motion';
import { FiUsers, FiFileText } from 'react-icons/fi';

export default function AdminDashboard() {
    const [users, setUsers] = useState([]);
    const [selectedUser, setSelectedUser] = useState(null);
    const [timesheets, setTimesheets] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchUsers = async () => {
            const response = await apiService.getAllUsers();
            setUsers(response.data.data || []);
        };
        fetchUsers();
    }, []);

    const handleUserSelect = async (user) => {
        setSelectedUser(user);
        setLoading(true);
        try {
            const response = await apiService.getTimesheetsByUserId(user.user_id);
            setTimesheets(response.data.data || []);
        } catch (error) { 
            console.error("Failed to fetch user timesheets", error);
        } finally { 
            setLoading(false); 
        }
    };

    return (
        <div className="container mx-auto p-6">
            <h1 className="text-3xl font-bold text-text-primary mb-6">Administrator Dashboard</h1>
            <div className="grid md:grid-cols-12 gap-6 items-start">
                {/* Employee List Panel */}
                <motion.div 
                  className="md:col-span-4 bg-primary border border-border p-6 rounded-lg shadow-sm"
                  initial={{ opacity: 0, x: -30 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ type: "spring", stiffness: 300, damping: 25 }}
                >
                    <h2 className="text-xl font-bold mb-4 text-text-primary flex items-center space-x-2">
                        <FiUsers />
                        <span>Employees</span>
                    </h2>
                    <ul className="space-y-2 max-h-[60vh] overflow-y-auto">
                        {users.map(user => (
                            <li 
                                key={user.user_id} 
                                onClick={() => handleUserSelect(user)}
                                className={`p-3 rounded-md cursor-pointer font-medium transition-colors ${selectedUser?.user_id === user.user_id ? 'bg-accent text-white' : 'hover:bg-secondary text-text-secondary'}`}
                            >
                                {user.full_name}
                            </li>
                        ))}
                    </ul>
                </motion.div>

                {/* Work Logs Panel */}
                <motion.div 
                  className="md:col-span-8 bg-primary border border-border rounded-lg shadow-sm"
                  initial={{ opacity: 0, x: 30 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ type: "spring", stiffness: 300, damping: 25, delay: 0.1 }}
                >
                    <h2 className="text-xl font-bold p-6 text-text-primary flex items-center space-x-2">
                        <FiFileText />
                        <span>
                            {selectedUser ? `${selectedUser.full_name}'s Work Logs` : 'Select an Employee'}
                        </span>
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="min-w-full text-sm">
                            <thead className="bg-secondary">
                                <tr>
                                    <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Date</th>
                                    <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Machine</th>
                                    <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Description</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border">
                                {loading ? (
                                    <tr><td colSpan="3" className="text-center py-8 text-text-secondary">Loading...</td></tr>
                                ) : timesheets.length > 0 ? timesheets.map((ts) => (
                                    <tr key={ts.id} className="hover:bg-secondary transition-colors">
                                        <td className="px-6 py-4">{ts.date}</td>
                                        <td className="px-6 py-4">{ts.machine}</td>
                                        <td className="px-6 py-4 text-text-secondary">{ts.description}</td>
                                    </tr>
                                )) : (
                                    <tr><td colSpan="3" className="text-center py-8 text-text-secondary">
                                        {selectedUser ? 'No work logs found for this user.' : 'Please select an employee to see their logs.'}
                                    </td></tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}