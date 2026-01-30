#!/bin/bash

# Create all remaining essential files

# Main App.jsx
cat > src/App.jsx << 'EOFAPP'
import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Login from './components/Auth/Login';
import SignUp from './components/Auth/SignUp';
import ForgotPassword from './components/Auth/ForgotPassword';
import DashboardLayout from './components/Layout/DashboardLayout';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-animated flex items-center justify-center">
        <div className="loading w-12 h-12"></div>
      </div>
    );
  }

  return (
    <>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#22c55e',
              secondary: '#fff',
            },
          },
          error: {
            duration: 4000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
      <BrowserRouter>
        <Routes>
          <Route
            path="/login"
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <Login setIsAuthenticated={setIsAuthenticated} />
              )
            }
          />
          <Route
            path="/signup"
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <SignUp />
              )
            }
          />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route
            path="/*"
            element={
              isAuthenticated ? (
                <DashboardLayout setIsAuthenticated={setIsAuthenticated} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
EOFAPP

# Create main.jsx
cat > src/main.jsx << 'EOFMAIN'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
EOFMAIN

# Create DashboardLayout
cat > src/components/Layout/DashboardLayout.jsx << 'EOFLAYOUT'
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
EOFLAYOUT

# Simple Dashboard
cat > src/components/Dashboard/Dashboard.jsx << 'EOFDASH'
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiServer, FiActivity, FiBell, FiTrendingUp, FiCpu, FiHardDrive } from 'react-icons/fi';
import { metricsAPI } from '../../services/api';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSummary();
    const interval = setInterval(fetchSummary, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchSummary = async () => {
    try {
      const response = await metricsAPI.getDashboardSummary();
      setSummary(response.data);
    } catch (error) {
      console.error('Error fetching summary:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="loading w-12 h-12"></div>
      </div>
    );
  }

  const stats = [
    {
      label: 'Total Instances',
      value: summary?.total_instances || 0,
      icon: FiServer,
      color: 'from-blue-500 to-blue-600',
      change: '+12%',
    },
    {
      label: 'Active Instances',
      value: summary?.active_instances || 0,
      icon: FiActivity,
      color: 'from-green-500 to-green-600',
      change: '+5%',
    },
    {
      label: 'Active Alerts',
      value: summary?.total_alerts || 0,
      icon: FiBell,
      color: 'from-yellow-500 to-yellow-600',
      change: '-3%',
    },
    {
      label: 'Avg CPU Usage',
      value: `${summary?.average_cpu?.toFixed(1) || 0}%`,
      icon: FiCpu,
      color: 'from-purple-500 to-purple-600',
      change: '+2%',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-8 bg-gradient-animated text-white"
      >
        <h1 className="text-4xl font-display font-bold mb-2">
          Welcome Back! 👋
        </h1>
        <p className="text-white/90">
          Here's what's happening with your infrastructure today
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="stat-card hover-lift"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center shadow-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <span className="badge-success">{stat.change}</span>
            </div>
            <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              {stat.value}
            </h3>
            <p className="text-gray-600 dark:text-gray-400">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      {/* Additional Info */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card p-6"
        >
          <h3 className="text-xl font-bold mb-4">Quick Stats</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Average Memory</span>
              <span className="font-semibold">{summary?.average_memory?.toFixed(1) || 0}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Average Disk</span>
              <span className="font-semibold">{summary?.average_disk?.toFixed(1) || 0}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Critical Alerts</span>
              <span className="font-semibold text-danger-600">{summary?.critical_alerts || 0}</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card p-6 bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20"
        >
          <h3 className="text-xl font-bold mb-4">Getting Started</h3>
          <ul className="space-y-3">
            <li className="flex items-center space-x-3">
              <div className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm">1</div>
              <span>Add your first EC2 instance</span>
            </li>
            <li className="flex items-center space-x-3">
              <div className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm">2</div>
              <span>Configure alert thresholds</span>
            </li>
            <li className="flex items-center space-x-3">
              <div className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm">3</div>
              <span>View real-time metrics</span>
            </li>
          </ul>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
EOFDASH

echo "All components created successfully!"
