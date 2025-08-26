import React, { useState, useEffect, useCallback } from 'react';
import apiService from '../services/apiService';
import { motion } from 'framer-motion';
import { FiPlusCircle } from 'react-icons/fi';

const TimesheetForm = ({ onUpdate }) => {
    // Form logic remains the same
    const [formData, setFormData] = useState({ machine: '', description: '', date: new Date().toISOString().split('T')[0], start_time: '', end_time: '' });
    const [error, setError] = useState('');
    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });
    const handleSubmit = async (e) => {
        e.preventDefault(); setError('');
        try {
            await apiService.createTimesheet(formData);
            onUpdate();
            setFormData({ machine: '', description: '', date: new Date().toISOString().split('T')[0], start_time: '', end_time: '' });
        } catch (err) { setError(err.response?.data?.message || 'Failed to submit timesheet.'); }
    };

    return (
        <motion.form onSubmit={handleSubmit} className="bg-primary border border-border p-6 rounded-lg space-y-4 mb-8 shadow-sm"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 25 }}
        >
            <h2 className="text-2xl font-bold text-text-primary">Log New Work</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                <input name="machine" placeholder="Machine Name/ID" onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md" />
                <input name="date" type="date" value={formData.date} onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md" />
                <input name="start_time" type="time" onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md" />
                <input name="end_time" type="time" onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md" />
            </div>
            <textarea name="description" placeholder="Task Description..." onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md min-h-[80px]" />
            <button type="submit" className="w-full py-2 bg-accent text-white font-semibold rounded-md flex items-center justify-center space-x-2">
              <FiPlusCircle /> <span>Submit Work Log</span>
            </button>
            {error && <p className="text-red-500">{error}</p>}
        </motion.form>
    );
};

export default function Dashboard({ user }) {
    const [timesheets, setTimesheets] = useState([]);
    const fetchTimesheets = useCallback(async () => {
        try {
            const response = await apiService.getMyTimesheets();
            setTimesheets(response.data.data || []);
        } catch (error) { console.error("Failed to fetch timesheets", error); }
    }, []);

    useEffect(() => { fetchTimesheets(); }, [fetchTimesheets]);

    return (
        <div className="container mx-auto p-6">
            <h1 className="text-3xl font-bold text-text-primary mb-6">Welcome, {user?.full_name || 'Employee'}!</h1>
            <TimesheetForm onUpdate={fetchTimesheets} />
            <div className="bg-primary border border-border rounded-lg shadow-sm overflow-hidden">
                <h2 className="text-2xl font-bold text-text-primary p-6">Your Work Logs</h2>
                <div className="overflow-x-auto">
                    <table className="min-w-full text-sm">
                        <thead className="bg-secondary">
                            <tr>
                                <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Date</th>
                                <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Machine</th>
                                <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Description</th>
                                <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Time</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                            {timesheets.map((ts) => (
                                <tr key={ts.id} className="hover:bg-secondary transition-colors">
                                    <td className="px-6 py-4 text-text-primary">{ts.date}</td>
                                    <td className="px-6 py-4 text-text-primary">{ts.machine}</td>
                                    <td className="px-6 py-4 text-text-secondary">{ts.description}</td>
                                    <td className="px-6 py-4 text-text-primary">{ts.start_time} - {ts.end_time}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}