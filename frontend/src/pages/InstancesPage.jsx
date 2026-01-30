import React from 'react';
import { Server } from 'lucide-react';

const InstancesPage = () => {
  return (
    <div className="space-y-6 animate-in">
      <div>
        <h1 className="text-3xl font-bold gradient-text">Instances</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your EC2 instances</p>
      </div>
      
      <div className="glass-card p-12 text-center">
        <Server className="w-16 h-16 text-primary-500 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          Instance Management
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Full instance management interface coming soon
        </p>
      </div>
    </div>
  );
};

export default InstancesPage;
