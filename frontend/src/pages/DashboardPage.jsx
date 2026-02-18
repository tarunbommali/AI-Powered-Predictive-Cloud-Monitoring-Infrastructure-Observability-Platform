import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { metricsAPI, instancesAPI } from '../services/api';
import { Server, Activity, AlertTriangle, TrendingUp, Cpu, HardDrive } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAutoRefresh } from '../hooks/useAutoRefresh';
import RefreshControl from '../components/RefreshControl';

const DashboardPage = () => {
  const [summary, setSummary] = useState(null);
  const [instances, setInstances] = useState([]);

  const fetchData = useCallback(async () => {
    try {
      const [summaryRes, instancesRes] = await Promise.all([
        metricsAPI.getDashboardSummary(),
        instancesAPI.list(),
      ]);
      setSummary(summaryRes.data);
      setInstances(instancesRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to fetch dashboard data');
    }
  }, []);

  const { loading, refreshing, refreshInterval, setRefreshInterval, manualRefresh } =
    useAutoRefresh(fetchData, 15, 300);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Dashboard</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Real-time monitoring overview</p>
        </div>
        <RefreshControl
          refreshInterval={refreshInterval}
          setRefreshInterval={setRefreshInterval}
          refreshing={refreshing}
          onManualRefresh={manualRefresh}
        />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={<Server className="w-6 h-6" />}
          title="Total Instances"
          value={summary?.total_instances || 0}
          gradient="from-blue-500 to-blue-600"
        />
        <StatCard
          icon={<Activity className="w-6 h-6" />}
          title="Active Instances"
          value={summary?.active_instances || 0}
          gradient="from-green-500 to-green-600"
        />
        <StatCard
          icon={<AlertTriangle className="w-6 h-6" />}
          title="Active Alerts"
          value={summary?.total_alerts || 0}
          gradient="from-yellow-500 to-yellow-600"
        />
        <StatCard
          icon={<TrendingUp className="w-6 h-6" />}
          title="Critical Alerts"
          value={summary?.critical_alerts || 0}
          gradient="from-red-500 to-red-600"
        />
      </div>

      {/* Average Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          title="Average CPU"
          value={summary?.average_cpu?.toFixed(1) || '0.0'}
          icon={<Cpu className="w-8 h-8" />}
          color="primary"
        />
        <MetricCard
          title="Average Memory"
          value={summary?.average_memory?.toFixed(1) || '0.0'}
          icon={<HardDrive className="w-8 h-8" />}
          color="secondary"
        />
        <MetricCard
          title="Average Disk"
          value={summary?.average_disk?.toFixed(1) || '0.0'}
          icon={<HardDrive className="w-8 h-8" />}
          color="success"
        />
      </div>

      {/* Instances List */}
      <div className="glass-card p-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          Instances ({instances.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {instances.map((instance) => (
            <InstanceCard key={instance.id} instance={instance} />
          ))}
          {instances.length === 0 && (
            <div className="col-span-full text-center py-12">
              <Server className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
              <p className="text-gray-500 dark:text-gray-400">No instances found</p>
              <p className="text-sm text-gray-400 dark:text-gray-500">Add an instance to get started</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, gradient }) => (
  <motion.div
    whileHover={{ y: -5 }}
    className="stat-card"
  >
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{title}</p>
        <p className="text-3xl font-bold text-gray-900 dark:text-white">{value}</p>
      </div>
      <div className={`p-3 bg-gradient-to-br ${gradient} rounded-xl text-white`}>
        {icon}
      </div>
    </div>
  </motion.div>
);

const MetricCard = ({ title, value, icon, color }) => {
  const colors = {
    primary: 'from-primary-500 to-primary-600',
    secondary: 'from-secondary-500 to-secondary-600',
    success: 'from-success-500 to-success-600',
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`glass-card p-6 bg-gradient-to-br ${colors[color]} text-white`}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-semibold">{title}</h3>
        {icon}
      </div>
      <p className="text-4xl font-bold">{value}%</p>
    </motion.div>
  );
};

const InstanceCard = ({ instance }) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    className="glass-card p-4"
  >
    <div className="flex items-start justify-between mb-3">
      <div className="flex items-center space-x-2">
        <Server className="w-5 h-5 text-primary-600" />
        <h3 className="font-semibold text-gray-900 dark:text-white">{instance.name}</h3>
      </div>
      <span className={`px-2 py-1 text-xs rounded-full ${instance.status === 'active'
          ? 'bg-success-100 text-success-700 dark:bg-success-900/30 dark:text-success-400'
          : 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400'
        }`}>
        {instance.status}
      </span>
    </div>
    <div className="space-y-1 text-sm">
      <p className="text-gray-600 dark:text-gray-400">
        <span className="font-medium">ID:</span> {instance.instance_id}
      </p>
      <p className="text-gray-600 dark:text-gray-400">
        <span className="font-medium">IP:</span> {instance.ip_address}
      </p>
      {instance.region && (
        <p className="text-gray-600 dark:text-gray-400">
          <span className="font-medium">Region:</span> {instance.region}
        </p>
      )}
    </div>
  </motion.div>
);

export default DashboardPage;
