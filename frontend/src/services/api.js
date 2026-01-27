import axios from 'axios';

// API Base URL - configure based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getMe: () => api.get('/auth/me'),
};

// Metrics API
export const metricsAPI = {
  getCPU: (instanceId) => api.get(`/metrics/cpu/${instanceId}`),
  getMemory: (instanceId) => api.get(`/metrics/memory/${instanceId}`),
  getDisk: (instanceId) => api.get(`/metrics/disk/${instanceId}`),
  getNetwork: (instanceId) => api.get(`/metrics/network/${instanceId}`),
  getLoad: (instanceId) => api.get(`/metrics/load/${instanceId}`),
  getAll: (instanceId) => api.get(`/metrics/all/${instanceId}`),
  getDashboardSummary: () => api.get('/metrics/dashboard/summary'),
};

// Instances API
export const instancesAPI = {
  list: () => api.get('/instances/'),
  get: (id) => api.get(`/instances/${id}`),
  create: (data) => api.post('/instances/', data),
  update: (id, data) => api.put(`/instances/${id}`, data),
  delete: (id) => api.delete(`/instances/${id}`),
  getAlerts: (id) => api.get(`/instances/${id}/alerts`),
};

// Health API
export const healthAPI = {
  check: () => api.get('/health/'),
  checkServices: () => api.get('/health/services'),
};

export default api;
