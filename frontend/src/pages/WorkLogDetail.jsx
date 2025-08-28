import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import apiService from '../services/apiService';
import { FiClock, FiTool, FiFileText, FiUser, FiCalendar, FiArrowLeft } from 'react-icons/fi';

const DetailField = ({ icon, label, children }) => (
    <div className="py-4 border-b border-border">
        <p className="text-sm font-semibold text-text-secondary flex items-center space-x-2">
            {icon}
            <span>{label}</span>
        </p>
        <div className="text-lg text-text-primary mt-1">{children}</div>
    </div>
);

export default function WorkLogDetail() {
    const { timesheetId } = useParams();
    const [log, setLog] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchLog = async () => {
            try {
                const response = await apiService.getTimesheetById(timesheetId);
                setLog(response.data.data);
            } catch (error) {
                console.error("Failed to fetch work log details", error);
            } finally {
                setLoading(false);
            }
        };
        fetchLog();
    }, [timesheetId]);

    if (loading) {
        return <div className="text-center p-10">Loading work log details...</div>;
    }
    
    if (!log) {
        return <div className="text-center p-10 text-red-500">Could not load work log details.</div>;
    }

    return (
        <div className="container mx-auto p-6">
            <motion.div
                className="max-w-3xl mx-auto bg-primary p-8 rounded-lg shadow-md border border-border"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", stiffness: 300, damping: 25 }}
            >
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <h1 className="text-3xl font-bold text-text-primary">Work Log Details</h1>
                        <p className="text-text-secondary">Entry ID: {log.id}</p>
                    </div>
                    <Link to={-1} className="flex items-center space-x-2 text-accent font-semibold hover:underline">
                        <FiArrowLeft />
                        <span>Go Back</span>
                    </Link>
                </div>

                <div className="space-y-2">
                    <DetailField icon={<FiUser />} label="Employee Name">
                        <p>{log.user.full_name}</p>
                    </DetailField>
                    <DetailField icon={<FiTool />} label="Machine">
                        <p>{log.machine}</p>
                    </DetailField>
                    <DetailField icon={<FiCalendar />} label="Date">
                        <p>{log.date}</p>
                    </DetailField>
                    <DetailField icon={<FiClock />} label="Time Spent">
                        <p>{log.start_time} - {log.end_time}</p>
                    </DetailField>
                    <DetailField icon={<FiFileText />} label="Description">
                        <p className="whitespace-pre-wrap text-text-secondary">{log.description}</p>
                    </DetailField>
                </div>
            </motion.div>
        </div>
    );
}