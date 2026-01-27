import React, { useState, useEffect } from 'react';
import { metricsAPI, instancesAPI } from '../services/api';
import { Activity, Server, AlertTriangle, TrendingUp, Cpu, HardDrive, Network, Clock } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [instances, setInstances] = useState([]);
  const [selectedInstance, setSelectedInstance] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, [selectedInstance]);

  const fetchData = async () => {
    try {
      const [summaryRes, instancesRes] = await Promise.all([
        metricsAPI.getDashboardSummary(),
        instancesAPI.list(),
      ]);
      
      setSummary(summaryRes.data);
      setInstances(instancesRes.data);
      
      if (!selectedInstance && instancesRes.data.length > 0) {
        setSelectedInstance(instancesRes.data[0].id);
      }
      
      if (selectedInstance) {
        const metricsRes = await metricsAPI.getAll(selectedInstance);
        setMetrics(metricsRes.data);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">Real-time monitoring overview</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Server}
          title="Total Instances"
          value={summary?.total_instances || 0}
          color="blue"
        />
        <StatCard
          icon={Activity}
          title="Active Instances"
          value={summary?.active_instances || 0}
          color="green"
        />
        <StatCard
          icon={AlertTriangle}
          title="Active Alerts"
          value={summary?.total_alerts || 0}
          color="yellow"
        />
        <StatCard
          icon={TrendingUp}
          title="Critical Alerts"
          value={summary?.critical_alerts || 0}
          color="red"
        />
      </div>

      {/* Instance Selector */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Select Instance
        </label>
        <select
          value={selectedInstance || ''}
          onChange={(e) => setSelectedInstance(parseInt(e.target.value))}
          className="w-full md:w-64 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        >
          {instances.map((instance) => (
            <key={instance.id} value={instance.id}>
              {instance.name} ({instance.instance_id})
            </option>
          ))}
        </select>
      </div>

      {/* Metrics Cards */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard
            icon={Cpu}
            title="CPU Usage"
            value={`${metrics.cpu.usage_percent.toFixed(1)}%`}
            threshold={80}
            current={metrics.cpu.usage_percent}
          />
          <MetricCard
            icon={HardDrive}
            title="Memory Usage"
            value={`${metrics.memory.usage_percent.toFixed(1)}%`}
            threshold={85}
            current={metrics.memory.usage_percent}
          />
          <MetricCard
            icon={HardDrive}
            title="Disk Usage"
            value={`${metrics.disk.usage_percent.toFixed(1)}%`}
            threshold={90}
            current={metrics.disk.usage_percent}
          />
          <MetricCard
            icon={Clock}
            title="Uptime"
            value={formatUptime(metrics.uptime_seconds)}
            threshold={100}
            current={0}
          />
        </div>
      )}

      {/* Average Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <AvgMetricCard
          title="Average CPU"
          value={summary?.average_cpu || 0}
          color="blue"
        />
        <AvgMetricCard
          title="Average Memory"
          value={summary?.average_memory || 0}
          color="purple"
        />
        <AvgMetricCard
          title="Average Disk"
          value={summary?.average_disk || 0}
          color="orange"
        />
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, title, value, color }) => {
  const colors = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    red: 'bg-red-500',
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{title}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{value}</p>
        </div>
        <div className={`${colors[color]} p-3 rounded-full`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ icon: Icon, title, value, threshold, current }) => {
  const getColor = () => {
    if (current >= threshold) return 'text-red-600';
    if (current >= threshold * 0.8) return 'text-yellow-600';
    return 'text-green-600';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center mb-4">
        <Icon className="w-5 h-5 text-gray-600 dark:text-gray-400 mr-2" />
        <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</h3>
      </div>
      <p className={`text-3xl font-bold ${getColor()}`}>{value}</p>
    </div>
  );
};

const AvgMetricCard = ({ title, value, color }) => {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
  };

  return (
    <div className={`bg-gradient-to-r ${colors[color]} rounded-lg shadow p-6 text-white`}>
      <h3 className="text-sm font-medium mb-2">{title}</h3>
      <p className="text-4xl font-bold">{value.toFixed(1)}%</p>
    </div>
  );
};

const formatUptime = (seconds) => {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return `${days}d ${hours}h ${minutes}m`;
};

export default Dashboard;
