import React, { useState, useEffect } from 'react';
import { instancesAPI } from '../services/api';
import { AlertTriangle, CheckCircle, XCircle, Clock } from 'lucide-react';
import { format } from 'date-fns';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [instances, setInstances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const instancesRes = await instancesAPI.list();
      setInstances(instancesRes.data);

      const allAlerts = [];
      for (const instance of instancesRes.data) {
        try {
          const alertsRes = await instancesAPI.getAlerts(instance.id);
          allAlerts.push(...alertsRes.data.map(alert => ({
            ...alert,
            instance_name: instance.name,
          })));
        } catch (error) {
          console.error(`Error fetching alerts for instance ${instance.id}:`, error);
        }
      }

      setAlerts(allAlerts);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const filteredAlerts = alerts.filter(alert => {
    if (filter === 'all') return true;
    if (filter === 'active') return alert.status === 'active';
    if (filter === 'resolved') return alert.status === 'resolved';
    if (filter === 'critical') return alert.severity === 'critical';
    if (filter === 'warning') return alert.severity === 'warning';
    return true;
  });

  const alertsByType = {
    cpu: filteredAlerts.filter(a => a.alert_type === 'cpu').length,
    memory: filteredAlerts.filter(a => a.alert_type === 'memory').length,
    disk: filteredAlerts.filter(a => a.alert_type === 'disk').length,
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
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Alerts</h1>
        <p className="text-gray-600 dark:text-gray-400">Monitor system alerts and notifications</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title="Total Alerts" value={filteredAlerts.length} color="blue" />
        <StatCard title="CPU Alerts" value={alertsByType.cpu} color="purple" />
        <StatCard title="Memory Alerts" value={alertsByType.memory} color="green" />
        <StatCard title="Disk Alerts" value={alertsByType.disk} color="orange" />
      </div>

      {/* Filter */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <div className="flex flex-wrap gap-2">
          {['all', 'active', 'resolved', 'critical', 'warning'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg capitalize ${
                filter === f
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-12 text-center">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              No Alerts
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              All systems are operating normally
            </p>
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <AlertCard key={alert.id} alert={alert} />
          ))
        )}
      </div>
    </div>
  );
};

const StatCard = ({ title, value, color }) => {
  const colors = {
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
    green: 'bg-green-500',
    orange: 'bg-orange-500',
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{title}</p>
      <p className="text-3xl font-bold text-gray-900 dark:text-white">{value}</p>
    </div>
  );
};

const AlertCard = ({ alert }) => {
  const getSeverityColor = () => {
    if (alert.severity === 'critical') return 'border-l-red-500 bg-red-50 dark:bg-red-900/20';
    if (alert.severity === 'warning') return 'border-l-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
    return 'border-l-blue-500 bg-blue-50 dark:bg-blue-900/20';
  };

  const getSeverityIcon = () => {
    if (alert.status === 'resolved') return <CheckCircle className="w-6 h-6 text-green-500" />;
    if (alert.severity === 'critical') return <XCircle className="w-6 h-6 text-red-500" />;
    return <AlertTriangle className="w-6 h-6 text-yellow-500" />;
  };

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg shadow border-l-4 ${getSeverityColor()} p-6`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-4 flex-1">
          {getSeverityIcon()}
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                {alert.metric_name}
              </h3>
              <span className={`px-2 py-1 text-xs rounded-full ${
                alert.status === 'active'
                  ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                  : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              }`}>
                {alert.status}
              </span>
              <span className={`px-2 py-1 text-xs rounded-full ${
                alert.severity === 'critical'
                  ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                  : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
              }`}>
                {alert.severity}
              </span>
            </div>
            
            <p className="text-gray-700 dark:text-gray-300 mb-3">{alert.message}</p>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-600 dark:text-gray-400">Instance:</span>
                <p className="font-medium text-gray-900 dark:text-white">{alert.instance_name}</p>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Current Value:</span>
                <p className="font-medium text-gray-900 dark:text-white">
                  {alert.current_value.toFixed(2)}%
                </p>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Threshold:</span>
                <p className="font-medium text-gray-900 dark:text-white">
                  {alert.threshold_value.toFixed(2)}%
                </p>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Triggered:</span>
                <p className="font-medium text-gray-900 dark:text-white flex items-center">
                  <Clock className="w-3 h-3 mr-1" />
                  {format(new Date(alert.triggered_at), 'HH:mm:ss')}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Alerts;
