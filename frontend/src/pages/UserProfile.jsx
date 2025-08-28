import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiUser, FiMail, FiPhone, FiCalendar, FiShield, FiEdit, FiSave, FiXCircle } from 'react-icons/fi';
import apiService from '../services/apiService';

const ProfileField = ({ icon, label, value, isEditing = false, name, onChange, type = 'text' }) => (
    <div className="flex items-center space-x-4 py-4 border-b border-border">
        <div className="text-accent text-xl mt-1">{icon}</div>
        <div className="flex-1">
            <p className="text-sm font-semibold text-text-secondary">{label}</p>
            {isEditing ? (
                <input
                    type={type}
                    name={name}
                    value={value || ''}
                    onChange={onChange}
                    className="w-full text-lg text-text-primary bg-secondary p-1 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
                />
            ) : (
                <p className="text-lg text-text-primary">{value || 'Not Provided'}</p>
            )}
        </div>
    </div>
);

export default function UserProfile({ user, setUser }) {
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({});
    
    const initializeFormData = (currentUser) => {
        if (currentUser) {
            setFormData({
                full_name: currentUser.full_name || '',
                dob: currentUser.dob || '',
                gender: currentUser.gender || '',
                email: currentUser.emails?.[0]?.email || '',
                phone_number: currentUser.phone_numbers?.[0]?.phone_number || '',
            });
        }
    };

    useEffect(() => {
        initializeFormData(user);
    }, [user]);

    if (!user) {
        return <div className="text-center p-10">Loading user profile...</div>;
    }
    
    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSave = async () => {
        try {
            const response = await apiService.updateUserProfile(formData);
            setUser(response.data.data);
            setIsEditing(false);
        } catch (error) {
            console.error("Failed to update profile", error);
        }
    };
    
    const handleCancel = () => {
        initializeFormData(user);
        setIsEditing(false);
    };

    return (
        <div className="container mx-auto p-6">
            <motion.div
                className="max-w-2xl mx-auto bg-primary p-8 rounded-lg shadow-md border border-border"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", stiffness: 300, damping: 25 }}
            >
                <div className="flex justify-between items-start mb-8">
                    <div className="text-left">
                        <h1 className="text-3xl font-bold text-text-primary">{isEditing ? formData.full_name : user.full_name}</h1>
                        <p className="text-text-secondary">{user.account?.role || 'Employee'}</p>
                    </div>
                    {isEditing ? (
                        <div className="flex space-x-2">
                            <button onClick={handleSave} className="p-2 bg-success text-white rounded-full hover:bg-green-600"><FiSave /></button>
                            <button onClick={handleCancel} className="p-2 bg-red-500 text-white rounded-full hover:bg-red-600"><FiXCircle /></button>
                        </div>
                    ) : (
                        <button onClick={() => setIsEditing(true)} className="p-2 bg-accent text-white rounded-full hover:bg-blue-700"><FiEdit /></button>
                    )}
                </div>
                <div className="space-y-2">
                    <ProfileField icon={<FiUser />} label="Full Name" name="full_name" value={formData.full_name} isEditing={isEditing} onChange={handleInputChange} />
                    <ProfileField icon={<FiMail />} label="Email (Primary)" name="email" value={formData.email} isEditing={isEditing} onChange={handleInputChange} type="email" />
                    <ProfileField icon={<FiPhone />} label="Phone (Primary)" name="phone_number" value={formData.phone_number} isEditing={isEditing} onChange={handleInputChange} />
                    <ProfileField icon={<FiCalendar />} label="Date of Birth" name="dob" value={formData.dob} isEditing={isEditing} onChange={handleInputChange} type="date" />
                    <ProfileField icon={<FiUser />} label="Gender" name="gender" value={formData.gender} isEditing={isEditing} onChange={handleInputChange} />
                    <ProfileField icon={<FiShield />} label="Account Status" value={user.account?.is_active ? 'Active' : 'Inactive'} />
                </div>
            </motion.div>
        </div>
    );
}