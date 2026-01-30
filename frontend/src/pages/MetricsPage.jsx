import React from 'react';
import { Activity } from 'lucide-react';

const MetricsPage = () => {
  return (
    <div className="space-y-6 animate-in">
      <div>
        <h1 className="text-3xl font-bold gradient-text">Metrics</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Detailed system metrics</p>
      </div>
      
      <div className="glass-card p-12 text-center">
        <Activity className="w-16 h-16 text-primary-500 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          Metrics Dashboard
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Real-time metrics visualization coming soon
        </p>
      </div>
    </div>
  );
};

export default MetricsPage;
