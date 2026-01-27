import React, { useState, useEffect } from 'react';
import { instancesAPI } from '../services/api';
import { Plus, Edit2, Trash2, Server, Circle } from 'lucide-react';

const Instances = () => {
  const [instances, setInstances] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingInstance, setEditingInstance] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    instance_id: '',
    ip_address: '',
    port: 9100,
    region: '',
    instance_type: '',
  });

  useEffect(() => {
    fetchInstances();
  }, []);

  const fetchInstances = async () => {
    try {
      const response = await instancesAPI.list();
      setInstances(response.data);
    } catch (error) {
      console.error('Error fetching instances:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingInstance) {
        await instancesAPI.update(editingInstance.id, formData);
      } else {
        await instancesAPI.create(formData);
      }
      setShowModal(false);
      setEditingInstance(null);
      resetForm();
      fetchInstances();
    } catch (error) {
      console.error('Error saving instance:', error);
      alert('Error saving instance: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this instance?')) {
      try {
        await instancesAPI.delete(id);
        fetchInstances();
      } catch (error) {
        console.error('Error deleting instance:', error);
      }
    }
  };

  const handleEdit = (instance) => {
    setEditingInstance(instance);
    setFormData({
      name: instance.name,
      instance_id: instance.instance_id,
      ip_address: instance.ip_address,
      port: instance.port,
      region: instance.region || '',
      instance_type: instance.instance_type || '',
    });
    setShowModal(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      instance_id: '',
      ip_address: '',
      port: 9100,
      region: '',
      instance_type: '',
    });
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Instances</h1>
          <p className="text-gray-600 dark:text-gray-400">Manage your EC2 instances</p>
        </div>
        <button
          onClick={() => {
            resetForm();
            setEditingInstance(null);
            setShowModal(true);
          }}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Instance
        </button>
      </div>

      {/* Instances Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {instances.map((instance) => (
          <div key={instance.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <Server className="w-6 h-6 text-blue-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {instance.name}
                </h3>
              </div>
              <div className="flex items-center">
                <Circle
                  className={`w-3 h-3 ${
                    instance.status === 'active' ? 'text-green-500 fill-green-500' : 'text-gray-400 fill-gray-400'
                  }`}
                />
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-gray-600 dark:text-gray-400">Instance ID:</span>
                <span className="ml-2 text-gray-900 dark:text-white font-mono">{instance.instance_id}</span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">IP Address:</span>
                <span className="ml-2 text-gray-900 dark:text-white font-mono">{instance.ip_address}:{instance.port}</span>
              </div>
              {instance.region && (
                <div>
                  <span className="text-gray-600 dark:text-gray-400">Region:</span>
                  <span className="ml-2 text-gray-900 dark:text-white">{instance.region}</span>
                </div>
              )}
              {instance.instance_type && (
                <div>
                  <span className="text-gray-600 dark:text-gray-400">Type:</span>
                  <span className="ml-2 text-gray-900 dark:text-white">{instance.instance_type}</span>
                </div>
              )}
            </div>

            <div className="mt-4 flex space-x-2">
              <button
                onClick={() => handleEdit(instance)}
                className="flex-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 px-3 py-2 rounded-lg flex items-center justify-center"
              >
                <Edit2 className="w-4 h-4 mr-1" />
                Edit
              </button>
              <button
                onClick={() => handleDelete(instance.id)}
                className="flex-1 bg-red-100 dark:bg-red-900 hover:bg-red-200 dark:hover:bg-red-800 text-red-700 dark:text-red-300 px-3 py-2 rounded-lg flex items-center justify-center"
              >
                <Trash2 className="w-4 h-4 mr-1" />
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {editingInstance ? 'Edit Instance' : 'Add Instance'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Instance ID *
                </label>
                <input
                  type="text"
                  required
                  value={formData.instance_id}
                  onChange={(e) => setFormData({ ...formData, instance_id: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  IP Address *
                </label>
                <input
                  type="text"
                  required
                  value={formData.ip_address}
                  onChange={(e) => setFormData({ ...formData, ip_address: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Port
                </label>
                <input
                  type="number"
                  value={formData.port}
                  onChange={(e) => setFormData({ ...formData, port: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Region
                  </label>
                  <input
                    type="text"
                    value={formData.region}
                    onChange={(e) => setFormData({ ...formData, region: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Type
                  </label>
                  <input
                    type="text"
                    value={formData.instance_type}
                    onChange={(e) => setFormData({ ...formData, instance_type: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
              </div>

              <div className="flex space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingInstance(null);
                    resetForm();
                  }}
                  className="flex-1 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
                >
                  {editingInstance ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Instances;
