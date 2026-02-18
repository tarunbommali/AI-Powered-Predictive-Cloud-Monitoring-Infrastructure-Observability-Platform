import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Server, Plus, Trash2, RefreshCw } from "lucide-react";
import { instancesAPI } from "../services/api";
import toast from "react-hot-toast";

const InstancesPage = () => {
  const [instances, setInstances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAdd, setShowAdd] = useState(false);
  const [formData, setFormData] = useState({
    name: "", instance_id: "", ip_address: "", port: 9100, region: "", instance_type: ""
  });

  useEffect(() => {
    fetchInstances();
  }, []);

  const fetchInstances = () => {
    setLoading(true);
    instancesAPI
      .list()
      .then((res) => setInstances(res.data))
      .catch((err) => {
        console.error("Error fetching instances:", err);
        toast.error("Failed to load instances");
      })
      .finally(() => setLoading(false));
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await instancesAPI.create(formData);
      toast.success("Instance added successfully!");
      setShowAdd(false);
      setFormData({ name: "", instance_id: "", ip_address: "", port: 9100, region: "", instance_type: "" });
      fetchInstances();
    } catch (err) {
      console.error("Error adding instance:", err);
      toast.error(err.response?.data?.detail || "Failed to add instance");
    }
  };

  const handleDelete = async (instanceId) => {
    if (!window.confirm("Are you sure you want to delete this instance?")) return;
    try {
      await instancesAPI.delete(instanceId);
      toast.success("Instance deleted");
      fetchInstances();
    } catch (err) {
      console.error("Error:", err);
      toast.error("Failed to delete instance");
    }
  };

  return (
    <div className="space-y-6 animate-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Instances</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Manage your EC2 instances
          </p>
        </div>
        <div className="flex items-center gap-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={fetchInstances}
            className="btn-outline flex items-center gap-2 text-sm"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowAdd(!showAdd)}
            className="btn-primary flex items-center gap-2 text-sm"
          >
            <Plus className="w-4 h-4" />
            Add Instance
          </motion.button>
        </div>
      </div>

      {/* Add Instance Form */}
      {showAdd && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-6"
        >
          <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Add New Instance</h3>
          <form onSubmit={handleAdd} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <input
              type="text" placeholder="Name (e.g. EC2 Production)" required
              value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })}
              className="px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
            />
            <input
              type="text" placeholder="Instance ID (e.g. i-0347ad...)" required
              value={formData.instance_id} onChange={e => setFormData({ ...formData, instance_id: e.target.value })}
              className="px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
            />
            <input
              type="text" placeholder="IP Address" required
              value={formData.ip_address} onChange={e => setFormData({ ...formData, ip_address: e.target.value })}
              className="px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
            />
            <input
              type="number" placeholder="Port (default: 9100)"
              value={formData.port} onChange={e => setFormData({ ...formData, port: parseInt(e.target.value) })}
              className="px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
            />
            <input
              type="text" placeholder="Region (e.g. ap-south-1)"
              value={formData.region} onChange={e => setFormData({ ...formData, region: e.target.value })}
              className="px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
            />
            <input
              type="text" placeholder="Instance Type (e.g. t2.micro)"
              value={formData.instance_type} onChange={e => setFormData({ ...formData, instance_type: e.target.value })}
              className="px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
            />
            <div className="sm:col-span-2 lg:col-span-3 flex gap-3">
              <button type="submit" className="btn-primary text-sm px-6">Add Instance</button>
              <button type="button" onClick={() => setShowAdd(false)} className="btn-outline text-sm px-6">Cancel</button>
            </div>
          </form>
        </motion.div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center min-h-[40vh]">
          <div className="spinner"></div>
        </div>
      )}

      {/* Empty State */}
      {!loading && instances.length === 0 && (
        <div className="glass-card p-12 text-center">
          <Server className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No Instances Found</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Add an instance to start monitoring
          </p>
        </div>
      )}

      {/* Instances Table */}
      {!loading && instances.length > 0 && (
        <div className="glass-card overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="p-4 text-left text-sm font-semibold text-gray-900 dark:text-white">Name</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-900 dark:text-white">Instance ID</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-900 dark:text-white">IP Address</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-900 dark:text-white">Status</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-900 dark:text-white">Region</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-900 dark:text-white">Type</th>
                <th className="p-4 text-left text-sm font-semibold text-gray-900 dark:text-white">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
              {instances.map((inst) => (
                <tr key={inst.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <Server className="w-4 h-4 text-primary-500" />
                      <span className="font-medium text-gray-900 dark:text-white text-sm">{inst.name}</span>
                    </div>
                  </td>
                  <td className="p-4 text-sm font-mono text-gray-600 dark:text-gray-400">{inst.instance_id}</td>
                  <td className="p-4 text-sm text-gray-600 dark:text-gray-400">{inst.ip_address}:{inst.port}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 text-xs rounded-full font-medium ${inst.status === 'active'
                        ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                        : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
                      }`}>
                      {inst.status}
                    </span>
                  </td>
                  <td className="p-4 text-sm text-gray-600 dark:text-gray-400">{inst.region || "—"}</td>
                  <td className="p-4 text-sm text-gray-600 dark:text-gray-400">{inst.instance_type || "—"}</td>
                  <td className="p-4">
                    <button
                      onClick={() => handleDelete(inst.instance_id)}
                      className="p-1.5 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg"
                      title="Delete instance"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default InstancesPage;
