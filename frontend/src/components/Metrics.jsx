import React, { useState, useEffect } from 'react';
import { metricsAPI, instancesAPI } from '../services/api';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { RefreshCw } from 'lucide-react';

const Metrics = () => {
  const [instances, setInstances] = useState([]);
  const [selectedInstance, setSelectedInstance] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    fetchInstances();
  }, []);

  useEffect(() => {
    if (selectedInstance) {
      fetchMetrics();
    }
    
    if (autoRefresh && selectedInstance) {
      const interval = setInterval(fetchMetrics, 5000);
      return () => clearInterval(interval);
    }
  }, [selectedInstance, autoRefresh]);

  const fetchInstances = async () => {
    try {
      const response = await instancesAPI.list();
      setInstances(response.data);
      if (response.data.length > 0) {
        setSelectedInstance(response.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching instances:', error);
    }
  };

  const fetchMetrics = async () => {
    if (!selectedInstance) return;
    
    setLoading(true);
    try {
      const response = await metricsAPI.getAll(selectedInstance);
      setMetrics(response.data);
      
      // Add to history
      setHistory(prev => {
        const newHistory = [...prev, {
          timestamp: new Date().toLocaleTimeString(),
          cpu: response.data.cpu.usage_percent,
          memory: response.data.memory.usage_percent,
          disk: response.data.disk.usage_percent,
        }];
        return newHistory.slice(-20); // Keep last 20 data points
      });
    } catch (error) {
      console.error('Error fetching metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">System Metrics</h1>
          <p className="text-gray-600 dark:text-gray-400">Detailed performance metrics</p>
        </div>
        <div className="flex items-center space-x-4">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="rounded"
            />
            <span className="text-sm text-gray-700 dark:text-gray-300">Auto Refresh</span>
          </label>
          <button
            onClick={fetchMetrics}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Instance Selector */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <select
          value={selectedInstance || ''}
          onChange={(e) => setSelectedInstance(parseInt(e.target.value))}
          className="w-full md:w-64 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        >
          {instances.map((instance) => (
            <option key={instance.id} value={instance.id}>
              {instance.name} ({instance.instance_id})
            </option>
          ))}
        </select>
      </div>

      {/* Metrics Charts */}
      {metrics && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* CPU Chart */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                CPU Usage
              </h3>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={history}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="timestamp" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="cpu" stroke="#3b82f6" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Memory Chart */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Memory Usage
              </h3>
              <ResponsiveContainer width="100%" height={250}>
                <AreaChart data={history}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="timestamp" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="memory" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.6} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Detailed Metrics */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* CPU Details */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">CPU Details</h3>
              <div className="space-y-2">
                <MetricRow label="Usage" value={`${metrics.cpu.usage_percent.toFixed(2)}%`} />
                <MetricRow label="Load (1m)" value={metrics.cpu.load_1min.toFixed(2)} />
                <MetricRow label="Load (5m)" value={metrics.cpu.load_5min.toFixed(2)} />
                <MetricRow label="Load (15m)" value={metrics.cpu.load_15min.toFixed(2)} />
                <MetricRow label="Cores" value={metrics.cpu.per_core?.length || 'N/A'} />
              </div>
            </div>

            {/* Memory Details */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Memory Details</h3>
              <div className="space-y-2">
                <MetricRow label="Usage" value={`${metrics.memory.usage_percent.toFixed(2)}%`} />
                <MetricRow label="Total" value={formatBytes(metrics.memory.total)} />
                <MetricRow label="Used" value={formatBytes(metrics.memory.used)} />
                <MetricRow label="Available" value={formatBytes(metrics.memory.available)} />
                <MetricRow label="Swap Used" value={formatBytes(metrics.memory.swap_used)} />
              </div>
            </div>

            {/* Disk Details */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Disk Details</h3>
              <div className="space-y-2">
                <MetricRow label="Usage" value={`${metrics.disk.usage_percent.toFixed(2)}%`} />
                <MetricRow label="Total" value={formatBytes(metrics.disk.total)} />
                <MetricRow label="Used" value={formatBytes(metrics.disk.used)} />
                <MetricRow label="Available" value={formatBytes(metrics.disk.available)} />
                <MetricRow label="Read" value={formatBytes(metrics.disk.read_bytes) + '/s'} />
                <MetricRow label="Write" value={formatBytes(metrics.disk.write_bytes) + '/s'} />
              </div>
            </div>
          </div>

          {/* Network Stats */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Network Statistics</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <MetricBox label="RX Bytes" value={formatBytes(metrics.network.rx_bytes) + '/s'} />
              <MetricBox label="TX Bytes" value={formatBytes(metrics.network.tx_bytes) + '/s'} />
              <MetricBox label="RX Packets" value={Math.round(metrics.network.rx_packets) + '/s'} />
              <MetricBox label="TX Packets" value={Math.round(metrics.network.tx_packets) + '/s'} />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

const MetricRow = ({ label, value }) => (
  <div className="flex justify-between text-sm">
    <span className="text-gray-600 dark:text-gray-400">{label}:</span>
    <span className="font-medium text-gray-900 dark:text-white">{value}</span>
  </div>
);

const MetricBox = ({ label, value }) => (
  <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{label}</p>
    <p className="text-lg font-semibold text-gray-900 dark:text-white">{value}</p>
  </div>
);

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
};

export default Metrics;
