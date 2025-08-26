import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiTrendingUp, FiDatabase, FiUsers } from 'react-icons/fi';

const popIn = {
  hidden: { scale: 0.8, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: { type: "spring", stiffness: 300, damping: 20 }
  }
};

const Feature = ({ icon, title, text }) => (
  <motion.div variants={popIn} className="bg-primary p-6 rounded-lg border border-border text-center">
    <div className="flex justify-center mb-4 text-accent text-3xl">{icon}</div>
    <h3 className="text-xl font-bold text-text-primary mb-2">{title}</h3>
    <p className="text-text-secondary">{text}</p>
  </motion.div>
);

export default function LandingPage() {
  return (
    <div className="bg-primary">
      {/* Hero Section */}
      <div className="container mx-auto px-6 py-24 text-center">
        <motion.h1 variants={popIn} initial="hidden" animate="visible" className="text-5xl md:text-6xl font-extrabold text-text-primary mb-4">
          Boost Your Team's Efficiency
        </motion.h1>
        <motion.p variants={popIn} initial="hidden" animate="visible" transition={{ delay: 0.2 }} className="text-lg text-text-secondary max-w-3xl mx-auto mb-8">
          WorkEntry is the all-in-one platform for small-scale manufacturing to track daily progress, manage tasks, and drive growth.
        </motion.p>
        <motion.div variants={popIn} initial="hidden" animate="visible" transition={{ delay: 0.4 }}>
          <Link to="/register" className="bg-accent text-white font-bold text-lg px-8 py-3 rounded-md shadow-lg hover:bg-blue-700 transition-transform hover:scale-105 inline-block">
            Start Your Free Trial
          </Link>
        </motion.div>
      </div>

      {/* Features Section */}
      <div className="bg-secondary py-20">
        <motion.div
          className="container mx-auto px-6"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.5 }}
          transition={{ staggerChildren: 0.2 }}
        >
          <h2 className="text-4xl font-bold text-center text-text-primary mb-12">Why Choose WorkEntry?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Feature icon={<FiDatabase />} title="Centralized Data" text="All your work logs and employee data in one secure, accessible place." />
            <Feature icon={<FiUsers />} title="Employee Management" text="Track individual performance and manage your team with ease." />
            <Feature icon={<FiTrendingUp />} title="Actionable Insights" text="Generate reports to understand productivity trends and make informed decisions." />
          </div>
        </motion.div>
      </div>
      
      {/* Final CTA Section */}
      <div className="bg-accent text-white text-center py-16">
        <h2 className="text-4xl font-bold mb-4">Ready to Transform Your Workflow?</h2>
        <p className="text-lg mb-8 opacity-90">Join leading manufacturing teams who trust WorkEntry.</p>
        <Link to="/register" className="bg-primary text-accent font-bold text-lg px-8 py-3 rounded-md shadow-lg hover:bg-gray-200 transition-transform hover:scale-105 inline-block">
          Sign Up Now
        </Link>
      </div>
    </div>
  );
}