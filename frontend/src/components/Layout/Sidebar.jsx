import React from 'react';
import { NavLink } from 'react-router-dom';
import { FiHome, FiActivity, FiServer, FiBell, FiBarChart2, FiSettings } from 'react-icons/fi';
import { motion } from 'framer-motion';

const Sidebar = ({ isOpen }) => {
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: FiHome },
    { path: '/metrics', label: 'Metrics', icon: FiActivity },
    { path: '/instances', label: 'Instances', icon: FiServer },
    { path: '/alerts', label: 'Alerts', icon: FiBell },
    { path: '/analytics', label: 'Analytics', icon: FiBarChart2 },
    { path: '/settings', label: 'Settings', icon: FiSettings },
  ];

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex lg:flex-col lg:w-64 glass-card border-r border-gray-200 dark:border-gray-700 min-h-screen">
        <nav className="flex-1 p-4 space-y-2">
          {navItems.map((item, index) => (
            <motion.div
              key={item.path}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all group ${
                    isActive
                      ? 'bg-gradient-primary text-white shadow-lg'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`
                }
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </NavLink>
            </motion.div>
          ))}
        </nav>

        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="glass rounded-xl p-4">
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Need Help?</h4>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Check our documentation for guides and tutorials.
            </p>
            <button className="btn-outline w-full text-sm">
              View Docs
            </button>
          </div>
        </div>
      </aside>

      {/* Mobile Sidebar */}
      {isOpen && (
        <motion.aside
          initial={{ x: -300 }}
          animate={{ x: 0 }}
          exit={{ x: -300 }}
          className="fixed inset-y-0 left-0 z-40 w-64 glass-card border-r border-gray-200 dark:border-gray-700 lg:hidden"
        >
          <nav className="flex-1 p-4 space-y-2 mt-20">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${
                    isActive
                      ? 'bg-gradient-primary text-white shadow-lg'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`
                }
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </motion.aside>
      )}

      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => {}}
        ></div>
      )}
    </>
  );
};

export default Sidebar;
