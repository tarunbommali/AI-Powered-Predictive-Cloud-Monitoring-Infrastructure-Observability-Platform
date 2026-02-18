#!/bin/bash

echo "============================================================"
echo "  Cloud Monitoring System - Backend Setup and Start"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Test dependencies
echo "Testing dependencies..."
python test_dependencies.py
echo ""

# Start backend
echo ""
echo "============================================================"
echo "  Starting Backend Server..."
echo "============================================================"
echo ""
python start_backend.py
