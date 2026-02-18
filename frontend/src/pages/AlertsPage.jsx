import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { instancesAPI } from '../services/api';
import { AlertTriangle, Bell, CheckCircle, Info, Server } from 'lucide-react';
import toast from 'react-hot-toast';

const AlertsPage = () => {
  const [instances, setInstances] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const res = await instancesAPI.list();
      setInstances(res.data);

      // Fetch alerts for all instances
      const allAlerts = [];
      for (const inst of res.data) {
        try {
          const alertRes = await instancesAPI.getAlerts(inst.instance_id);
          if (alertRes.data && alertRes.data.length > 0) {
            allAlerts.push(...alertRes.data.map(a => ({ ...a, instanceName: inst.name })));
          }
        } catch {
          // Instance may not have alerts
        }
      }
      setAlerts(allAlerts);
    } catch (err) {
      console.error('Error fetching alerts:', err);
      toast.error('Failed to load alerts');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-in">
      <div>
        <h1 className="text-3xl font-bold gradient-text">Alerts</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Monitor system alerts and notifications</p>
      </div>

      {/* Alert Thresholds Info */}
      <div className="glass-card p-5">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <Info className="w-5 h-5 text-blue-500" />
          Alert Thresholds
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <ThresholdCard label="CPU Usage" threshold="80%" color="blue" />
          <ThresholdCard label="Memory Usage" threshold="85%" color="yellow" />
          <ThresholdCard label="Disk Usage" threshold="90%" color="red" />
        </div>
      </div>

      {/* Active Alerts */}
      <div className="glass-card p-5">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <Bell className="w-5 h-5 text-yellow-500" />
          Active Alerts ({alerts.length})
        </h2>

        {alerts.length === 0 ? (
          <div className="text-center py-12">
            <CheckCircle className="w-16 h-16 text-green-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">All Clear</h3>
            <p className="text-gray-500 dark:text-gray-400">No active alerts. All systems are operating normally.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {alerts.map((alert, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className={`p-4 rounded-xl border-l-4 ${alert.severity === 'critical'
                    ? 'border-red-500 bg-red-50 dark:bg-red-900/10'
                    : alert.severity === 'warning'
                      ? 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/10'
                      : 'border-blue-500 bg-blue-50 dark:bg-blue-900/10'
                  }`}
              >
                <div className="flex items-start gap-3">
                  <AlertTriangle className={`w-5 h-5 mt-0.5 flex-shrink-0 ${alert.severity === 'critical' ? 'text-red-500' :
                      alert.severity === 'warning' ? 'text-yellow-500' : 'text-blue-500'
                    }`} />
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h4 className="font-semibold text-gray-900 dark:text-white text-sm">
                        {alert.alert_type || 'System Alert'}
                      </h4>
                      <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${alert.severity === 'critical'
                          ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                          : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
                        }`}>
                        {alert.severity}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{alert.message}</p>
                    <p className="text-xs text-gray-500 mt-1">{alert.instanceName} • {new Date(alert.created_at).toLocaleString()}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Monitored Instances */}
      <div className="glass-card p-5">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <Server className="w-5 h-5 text-primary-500" />
          Monitored Instances ({instances.length})
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {instances.map(inst => (
            <div key={inst.id} className="p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 flex items-center justify-between">
              <div>
                <p className="font-medium text-sm text-gray-900 dark:text-white">{inst.name}</p>
                <p className="text-xs text-gray-500">{inst.instance_id}</p>
              </div>
              <span className={`w-2.5 h-2.5 rounded-full ${inst.status === 'active' ? 'bg-green-500' : 'bg-gray-400'
                }`}></span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const ThresholdCard = ({ label, threshold, color }) => {
  const colors = {
    blue: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
    yellow: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
    red: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
  };
  return (
    <div className="p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 flex items-center justify-between">
      <span className="text-sm text-gray-700 dark:text-gray-300">{label}</span>
      <span className={`px-2 py-0.5 text-xs rounded-full font-bold ${colors[color]}`}>
        &gt; {threshold}
      </span>
    </div>
  );
};

export default AlertsPage;
