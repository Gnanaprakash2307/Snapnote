#!/bin/bash
# run.sh - Script to run the SnapNote application

# Create necessary directories
mkdir -p uploads/images
mkdir -p uploads/pdfs
mkdir -p uploads/notes

# Check if Python is installed
if command -v python3 &>/dev/null; then
    echo "Python 3 is installed"
else
    echo "Python 3 is not installed. Please install Python 3 to run this application."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install minimal required packages
echo "Installing required packages..."
pip install flask

# Create __init__.py files if they don't exist
touch utils/__init__.py

# Run the application
echo "Starting SnapNote application..."
python3 app.py