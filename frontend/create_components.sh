#!/bin/bash

# Header Component
cat > src/components/Header.jsx << 'ENDHEADER'
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { Cloud, Moon, Sun, LogOut, User, Menu, X } from 'lucide-react';
import { useState } from 'react';

const Header = () => {
  const { user, logout } = useAuth();
  const { darkMode, toggleDarkMode } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="glass border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center space-x-3">
            <motion.div
              whileHover={{ scale: 1.05, rotate: 5 }}
              className="p-2 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl"
            >
              <Cloud className="w-6 h-6 text-white" />
            </motion.div>
            <span className="text-xl font-bold gradient-text hidden sm:block">
              Cloud Monitor
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <NavLink to="/dashboard">Dashboard</NavLink>
            <NavLink to="/metrics">Metrics</NavLink>
            <NavLink to="/instances">Instances</NavLink>
            <NavLink to="/alerts">Alerts</NavLink>
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            {/* Theme Toggle */}
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={toggleDarkMode}
              className="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {darkMode ? (
                <Sun className="w-5 h-5 text-yellow-500" />
              ) : (
                <Moon className="w-5 h-5 text-gray-600" />
              )}
            </motion.button>

            {/* User Menu */}
            <div className="hidden md:flex items-center space-x-3">
              <div className="flex items-center space-x-2 px-3 py-2 bg-gray-100 dark:bg-gray-800 rounded-xl">
                <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
                <div className="hidden lg:block">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {user?.full_name || user?.username}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{user?.email}</p>
                </div>
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleLogout}
                className="p-2 text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-xl"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </motion.button>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="md:hidden py-4 space-y-2"
          >
            <MobileNavLink to="/dashboard" onClick={() => setMobileMenuOpen(false)}>
              Dashboard
            </MobileNavLink>
            <MobileNavLink to="/metrics" onClick={() => setMobileMenuOpen(false)}>
              Metrics
            </MobileNavLink>
            <MobileNavLink to="/instances" onClick={() => setMobileMenuOpen(false)}>
              Instances
            </MobileNavLink>
            <MobileNavLink to="/alerts" onClick={() => setMobileMenuOpen(false)}>
              Alerts
            </MobileNavLink>
            <button
              onClick={handleLogout}
              className="w-full text-left px-4 py-2 text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-xl"
            >
              Logout
            </button>
          </motion.div>
        )}
      </div>
    </header>
  );
};

const NavLink = ({ to, children }) => (
  <Link
    to={to}
    className="text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
  >
    {children}
  </Link>
);

const MobileNavLink = ({ to, children, onClick }) => (
  <Link
    to={to}
    onClick={onClick}
    className="block px-4 py-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-xl"
  >
    {children}
  </Link>
);

export default Header;
ENDHEADER

# Footer Component
cat > src/components/Footer.jsx << 'ENDFOOTER'
import React from 'react';
import { Link } from 'react-router-dom';
import { Cloud, Github, Twitter, Linkedin, Heart } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="glass border-t border-gray-200 dark:border-gray-700 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl">
                <Cloud className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">Cloud Monitor</span>
            </div>
            <p className="text-gray-600 dark:text-gray-400 max-w-md">
              Real-time infrastructure monitoring for modern cloud applications. Monitor AWS EC2 instances with ease and precision.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <FooterLink to="/dashboard">Dashboard</FooterLink>
              <FooterLink to="/metrics">Metrics</FooterLink>
              <FooterLink to="/instances">Instances</FooterLink>
              <FooterLink to="/alerts">Alerts</FooterLink>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Resources</h3>
            <ul className="space-y-2">
              <FooterLink to="#">Documentation</FooterLink>
              <FooterLink to="#">API Reference</FooterLink>
              <FooterLink to="#">Support</FooterLink>
              <FooterLink to="#">Status</FooterLink>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center space-x-1">
              <span>© {currentYear} Cloud Monitor. Made with</span>
              <Heart className="w-4 h-4 text-danger-500 fill-current" />
              <span>for DevOps Engineers</span>
            </p>
            
            <div className="flex items-center space-x-4">
              <SocialLink href="https://github.com" icon={<Github className="w-5 h-5" />} />
              <SocialLink href="https://twitter.com" icon={<Twitter className="w-5 h-5" />} />
              <SocialLink href="https://linkedin.com" icon={<Linkedin className="w-5 h-5" />} />
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

const FooterLink = ({ to, children }) => (
  <li>
    <Link
      to={to}
      className="text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
    >
      {children}
    </Link>
  </li>
);

const SocialLink = ({ href, icon }) => (
  <a
    href={href}
    target="_blank"
    rel="noopener noreferrer"
    className="p-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-all"
  >
    {icon}
  </a>
);

export default Footer;
ENDFOOTER

echo "Header and Footer created"
