import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiPlusCircle, FiClock } from 'react-icons/fi';
import apiService from '../services/apiService';

const TimesheetForm = ({ onUpdate }) => {
    // A robust function to get the current time in HH:MM format
    const getFormattedCurrentTime = () => {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        return `${hours}:${minutes}`;
    };

    const [formData, setFormData] = useState({ 
        machine: '', 
        description: '', 
        date: new Date().toISOString().split('T')[0], 
        start_time: getFormattedCurrentTime(), 
        end_time: getFormattedCurrentTime() 
    });
    
    const [error, setError] = useState('');
    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await apiService.createTimesheet(formData);
            onUpdate();
            // Reset form to new, valid current times
            setFormData({ 
                machine: '', 
                description: '', 
                date: new Date().toISOString().split('T')[0], 
                start_time: getFormattedCurrentTime(), 
                end_time: getFormattedCurrentTime() 
            });
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to submit timesheet.');
        }
    };

    return (
        <motion.form onSubmit={handleSubmit} className="bg-primary border border-border p-6 rounded-lg space-y-4 mb-8 shadow-sm"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 25 }}
        >
            <h2 className="text-2xl font-bold text-text-primary">Log New Work</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                <input name="machine" placeholder="Machine Name/ID" value={formData.machine} onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md" />
                <input name="date" type="date" value={formData.date} onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md" />
                <input name="start_time" type="time" value={formData.start_time} onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md" />
                <input name="end_time" type="time" value={formData.end_time} onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md" />
            </div>
            <textarea name="description" placeholder="Task Description..." value={formData.description} onChange={handleChange} required className="w-full px-4 py-2 border border-border rounded-md min-h-[80px]" />
            <button type="submit" className="w-full py-2 bg-accent text-white font-semibold rounded-md flex items-center justify-center space-x-2">
              <FiPlusCircle /> <span>Submit Work Log</span>
            </button>
            {error && <p className="text-red-500">{error}</p>}
        </motion.form>
    );
};

export default function Dashboard({ user }) {
    const navigate = useNavigate();
    
    const handleUpdate = () => {
        console.log("Work log submitted successfully!");
    };

    return (
        <div className="container mx-auto p-6">
            <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
                <h1 className="text-3xl font-bold text-text-primary mb-2">Welcome, {user?.full_name || 'Employee'}!</h1>
                <p className="text-text-secondary mb-8">Ready to log your work for the day?</p>
            </motion.div>
            
            <TimesheetForm onUpdate={handleUpdate} />

            <motion.div 
                className="bg-primary p-6 rounded-lg border border-border shadow-sm text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
            >
                <h2 className="text-xl font-bold text-text-primary mb-4">View Your History</h2>
                <p className="text-text-secondary mb-6">Access, search, and filter your complete work log history.</p>
                <button 
                    onClick={() => navigate('/my-work-logs')}
                    className="bg-accent text-white font-semibold px-6 py-3 rounded-md flex items-center justify-center space-x-2 mx-auto hover:bg-blue-700 transition-colors"
                >
                    <FiClock />
                    <span>View Full History</span>
                </button>
            </motion.div>
        </div>
    );
}