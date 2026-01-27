#!/bin/bash

# Cloud Monitoring System - Setup Script

set -e

echo "=================================="
echo "Cloud Monitoring System Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker Compose is installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your configuration before starting services"
else
    echo "✅ backend/.env already exists"
fi

echo ""
echo "Configuration:"
echo "1. Edit backend/.env with your settings"
echo "2. Edit monitoring/prometheus/prometheus.yml with your EC2 instance IPs"
echo "3. Edit monitoring/alertmanager/config.yml with your email settings"
echo ""

read -p "Have you configured the files? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please configure the files and run this script again."
    exit 0
fi

echo ""
echo "🚀 Starting services..."
echo ""

# Start services
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service health..."

# Check backend
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo "✅ Backend API is running"
else
    echo "⚠️  Backend API is not responding"
fi

# Check Prometheus
if curl -s http://localhost:9090/-/healthy > /dev/null; then
    echo "✅ Prometheus is running"
else
    echo "⚠️  Prometheus is not responding"
fi

# Check Grafana
if curl -s http://localhost:3001/api/health > /dev/null 2>&1; then
    echo "✅ Grafana is running"
else
    echo "⚠️  Grafana is not responding"
fi

echo ""
echo "=================================="
echo "Setup Complete! 🎉"
echo "=================================="
echo ""
echo "Access the application:"
echo "  Frontend:    http://localhost:3000"
echo "  Backend API: http://localhost:8000/api/docs"
echo "  Prometheus:  http://localhost:9090"
echo "  Grafana:     http://localhost:3001 (admin/admin)"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
echo "To register a user, use the frontend at http://localhost:3000"
echo ""
