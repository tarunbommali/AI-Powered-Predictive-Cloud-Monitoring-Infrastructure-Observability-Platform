#!/bin/bash

echo "============================================================"
echo "  Installing Backend Dependencies"
echo "============================================================"
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from your package manager"
    exit 1
fi
python3 --version
echo ""

echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists."
fi
echo ""

echo "Activating virtual environment..."
source venv/bin/activate
echo ""

echo "Installing dependencies from requirements.txt..."
echo "This may take a few minutes..."
echo ""
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "  SUCCESS: All dependencies installed!"
    echo "============================================================"
    echo ""
    echo "You can now start the backend with:"
    echo "  python start_backend.py"
    echo ""
    echo "Or create dummy users with:"
    echo "  python create_dummy_users.py"
    echo ""
else
    echo ""
    echo "============================================================"
    echo "  ERROR: Installation failed!"
    echo "============================================================"
    echo ""
    echo "Please check the error messages above."
    echo "Common issues:"
    echo "  - Internet connection required"
    echo "  - Some packages may need build tools"
    echo ""
    exit 1
fi
