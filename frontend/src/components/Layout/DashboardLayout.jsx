import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Header from './Header';
import Sidebar from './Sidebar';
import Footer from './Footer';
import Dashboard from '../Dashboard/Dashboard';
import toast from 'react-hot-toast';
import { authAPI } from '../../services/api';

const DashboardLayout = ({ setIsAuthenticated }) => {
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const isDark = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDark);
    if (isDark) {
      document.documentElement.classList.add('dark');
    }
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      const response = await authAPI.getMe();
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
    }
  };

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem('darkMode', newDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    toast.success('Logged out successfully');
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header
        darkMode={darkMode}
        toggleDarkMode={toggleDarkMode}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        handleLogout={handleLogout}
        user={user}
      />
      
      <div className="flex flex-1">
        <Sidebar isOpen={sidebarOpen} />
        
        <main className="flex-1 overflow-auto">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
            className="container mx-auto px-4 sm:px-6 lg:px-8 py-8"
          >
            <Routes>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/metrics" element={<div className="card p-8 text-center"><h2 className="text-2xl font-bold">Metrics Page - Coming Soon</h2></div>} />
              <Route path="/instances" element={<div className="card p-8 text-center"><h2 className="text-2xl font-bold">Instances Page - Coming Soon</h2></div>} />
              <Route path="/alerts" element={<div className="card p-8 text-center"><h2 className="text-2xl font-bold">Alerts Page - Coming Soon</h2></div>} />
              <Route path="/analytics" element={<div className="card p-8 text-center"><h2 className="text-2xl font-bold">Analytics Page - Coming Soon</h2></div>} />
              <Route path="/settings" element={<div className="card p-8 text-center"><h2 className="text-2xl font-bold">Settings Page - Coming Soon</h2></div>} />
            </Routes>
          </motion.div>
        </main>
      </div>
      
      <Footer />
    </div>
  );
};

export default DashboardLayout;
