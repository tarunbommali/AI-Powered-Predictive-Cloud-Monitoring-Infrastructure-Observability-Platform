#!/bin/bash

# Placeholder Pages
cat > src/pages/MetricsPage.jsx << 'ENDMETRICS'
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
ENDMETRICS

cat > src/pages/InstancesPage.jsx << 'ENDINST'
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
ENDINST

cat > src/pages/AlertsPage.jsx << 'ENDALERTS'
import React from 'react';
import { AlertTriangle } from 'lucide-react';

const AlertsPage = () => {
  return (
    <div className="space-y-6 animate-in">
      <div>
        <h1 className="text-3xl font-bold gradient-text">Alerts</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Monitor system alerts</p>
      </div>
      
      <div className="glass-card p-12 text-center">
        <AlertTriangle className="w-16 h-16 text-primary-500 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          Alert Dashboard
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Advanced alert monitoring coming soon
        </p>
      </div>
    </div>
  );
};

export default AlertsPage;
ENDALERTS

# Main App Component
cat > src/App.jsx << 'ENDAPP'
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { Toaster } from 'react-hot-toast';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import DashboardPage from './pages/DashboardPage';
import MetricsPage from './pages/MetricsPage';
import InstancesPage from './pages/InstancesPage';
import AlertsPage from './pages/AlertsPage';

// Components
import Layout from './components/Layout';

// Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

// Public Route wrapper (redirect if authenticated)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  return !isAuthenticated ? children : <Navigate to="/dashboard" replace />;
};

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'var(--toast-bg)',
                color: 'var(--toast-color)',
              },
              success: {
                iconTheme: {
                  primary: '#22c55e',
                  secondary: '#fff',
                },
              },
              error: {
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
          
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            } />
            <Route path="/register" element={
              <PublicRoute>
                <RegisterPage />
              </PublicRoute>
            } />
            <Route path="/forgot-password" element={
              <PublicRoute>
                <ForgotPasswordPage />
              </PublicRoute>
            } />

            {/* Protected Routes */}
            <Route path="/" element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="metrics" element={<MetricsPage />} />
              <Route path="instances" element={<InstancesPage />} />
              <Route path="alerts" element={<AlertsPage />} />
            </Route>

            {/* Catch all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
ENDAPP

# Main Entry Point
cat > src/main.jsx << 'ENDMAIN'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
ENDMAIN

# Dockerfile
cat > Dockerfile << 'ENDDOCKER'
FROM node:20-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
ENDDOCKER

# Nginx config
cat > nginx.conf << 'ENDNGINX'
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
ENDNGINX

# README
cat > README.md << 'ENDREADME'
# Cloud Monitoring Frontend

Beautiful, modern, and responsive frontend for the Cloud Monitoring System.

## Features

- 🎨 Modern UI with Tailwind CSS
- 🌓 Dark mode support
- 📱 Fully responsive design
- ✨ Smooth animations with Framer Motion
- 🔐 JWT authentication
- 🚀 Fast and optimized with Vite
- 📊 Real-time metrics visualization

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Access

- Development: http://localhost:3000
- Production: Configure in .env

## Environment Variables

Create a `.env` file:

```
VITE_API_URL=http://localhost:8000/api
```

## Tech Stack

- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Recharts
- React Router DOM
- Axios
- React Hot Toast

## License

MIT
ENDREADME

echo "All files created successfully!"
