import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import apiService from '../services/apiService';
import { motion } from 'framer-motion'; // <-- FIX: Add this missing import
import { FiSearch, FiFileText, FiArrowLeft } from 'react-icons/fi';

const FilterControls = ({ onFilterChange }) => {
    const [filters, setFilters] = useState({ machine: '', from_date: '', to_date: '' });
    const handleInputChange = (e) => setFilters({ ...filters, [e.target.name]: e.target.value });
    
    const handleSearch = () => {
        const activeFilters = Object.fromEntries(Object.entries(filters).filter(([_, v]) => v !== ''));
        onFilterChange(activeFilters);
    };

    return (
        <div className="bg-primary border-b border-border p-4 flex flex-wrap items-center gap-4">
            <input name="machine" placeholder="Search Machine..." value={filters.machine} onChange={handleInputChange} className="flex-grow px-4 py-2 border border-border rounded-md text-sm" />
            <input name="from_date" type="date" title="From Date" value={filters.from_date} onChange={handleInputChange} className="px-4 py-2 border border-border rounded-md text-sm" />
            <input name="to_date" type="date" title="To Date" value={filters.to_date} onChange={handleInputChange} className="px-4 py-2 border border-border rounded-md text-sm" />
            <button onClick={handleSearch} className="bg-accent text-white font-semibold px-4 py-2 rounded-md flex items-center space-x-2">
                <FiSearch /> <span>Search</span>
            </button>
        </div>
    );
};

export default function WorkLogsPage() {
    const [timesheets, setTimesheets] = useState([]);
    const [filters, setFilters] = useState({});
    const [pageTitle, setPageTitle] = useState("My Work Logs");
    const navigate = useNavigate();
    const { userId } = useParams();

    const fetchTimesheets = useCallback(async () => {
        try {
            const params = { ...filters, limit: 1000 };
            const response = userId 
                ? await apiService.getTimesheetsByUserId(userId, params)
                : await apiService.getMyTimesheets(params);
            
            setTimesheets(response.data.data || []);
            if(userId) setPageTitle("Employee Work Logs");

        } catch (error) { 
            console.error("Failed to fetch timesheets", error); 
        }
    }, [userId, filters]);

    useEffect(() => { 
        fetchTimesheets(); 
    }, [fetchTimesheets]);

    return (
        <div className="container mx-auto p-6">
             <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
                <Link to={-1} className="flex items-center space-x-2 text-accent font-semibold hover:underline mb-4">
                    <FiArrowLeft />
                    <span>Back to Dashboard</span>
                </Link>
                <h1 className="text-3xl font-bold text-text-primary mb-6">{pageTitle}</h1>
            </motion.div>

            <motion.div 
                className="bg-primary border border-border rounded-lg shadow-sm overflow-hidden"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
            >
                <FilterControls onFilterChange={setFilters} />
                <div className="overflow-x-auto max-h-[70vh] overflow-y-auto">
                    <table className="min-w-full text-sm">
                        <thead className="bg-secondary sticky top-0 z-10">
                            <tr>
                                <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Date</th>
                                <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Machine</th>
                                <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Description</th>
                                <th className="px-6 py-3 text-left font-semibold text-text-secondary uppercase">Time</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                            {timesheets.map((ts) => (
                                <tr 
                                  key={ts.id} 
                                  className="hover:bg-secondary transition-colors cursor-pointer"
                                  onClick={() => navigate(`/worklog/${ts.id}`)}
                                >
                                    <td className="px-6 py-4 text-text-primary">{ts.date}</td>
                                    <td className="px-6 py-4 text-text-primary">{ts.machine}</td>
                                    <td className="px-6 py-4 text-text-secondary">{ts.description}</td>
                                    <td className="px-6 py-4 text-text-primary">{ts.start_time} - {ts.end_time}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </motion.div>
        </div>
    );
}