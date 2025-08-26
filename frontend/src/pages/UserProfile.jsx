import React from 'react';
import { motion } from 'framer-motion';
import { FiUser, FiMail, FiPhone, FiCalendar, FiShield } from 'react-icons/fi';

// A reusable component for displaying profile information fields
const ProfileField = ({ icon, label, value }) => (
    <div className="flex items-start space-x-4 py-4 border-b border-border">
        <div className="text-accent text-xl">{icon}</div>
        <div>
            <p className="text-sm font-semibold text-text-secondary">{label}</p>
            <p className="text-lg text-text-primary">{value || 'Not Provided'}</p>
        </div>
    </div>
);

export default function UserProfile({ user }) {
    if (!user) {
        return <div className="text-center p-10">Loading user profile...</div>;
    }

    return (
        <div className="container mx-auto p-6">
            <motion.div
                className="max-w-2xl mx-auto bg-primary p-8 rounded-lg shadow-md border border-border"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", stiffness: 300, damping: 25 }}
            >
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-text-primary">{user.full_name}</h1>
                    <p className="text-text-secondary">{user.account?.role || 'Employee'}</p>
                </div>

                <div className="space-y-2">
                    <ProfileField icon={<FiUser />} label="Username" value={user.account?.username} />
                    <ProfileField icon={<FiMail />} label="Email" value={user.emails?.[0]?.email} />
                    <ProfileField icon={<FiPhone />} label="Phone Number" value={user.phone_numbers?.[0]?.phone_number} />
                    <ProfileField icon={<FiCalendar />} label="Date of Birth" value={user.dob} />
                    <ProfileField icon={<FiShield />} label="Account Status" value={user.account?.is_active ? 'Active' : 'Inactive'} />
                </div>
            </motion.div>
        </div>
    );
}