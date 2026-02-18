import React from 'react';
import { motion } from 'framer-motion';
import { RefreshCw, Clock } from 'lucide-react';
import { REFRESH_OPTIONS } from '../hooks/useAutoRefresh';

/**
 * Refresh control component with interval selector and manual refresh button
 */
const RefreshControl = ({ refreshInterval, setRefreshInterval, refreshing, onManualRefresh }) => {
    return (
        <div className="flex items-center gap-2">
            {/* Refresh Interval Selector */}
            <div className="flex items-center gap-1.5 px-2 py-1.5 rounded-xl bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <Clock className="w-3.5 h-3.5 text-gray-500 dark:text-gray-400" />
                <div className="flex gap-0.5">
                    {REFRESH_OPTIONS.map(opt => (
                        <button
                            key={opt.value}
                            onClick={() => setRefreshInterval(opt.value)}
                            className={`px-2 py-0.5 text-xs rounded-lg font-medium transition-all ${refreshInterval === opt.value
                                    ? 'bg-primary-500 text-white shadow-sm'
                                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
                                }`}
                        >
                            {opt.label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Manual Refresh */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onManualRefresh}
                disabled={refreshing}
                className="p-2 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                title="Refresh now"
            >
                <RefreshCw className={`w-4 h-4 text-gray-600 dark:text-gray-400 ${refreshing ? 'animate-spin' : ''}`} />
            </motion.button>

            {/* Live indicator */}
            {refreshInterval > 0 && (
                <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                    </span>
                    <span className="hidden sm:inline">Live</span>
                </div>
            )}
        </div>
    );
};

export default RefreshControl;
