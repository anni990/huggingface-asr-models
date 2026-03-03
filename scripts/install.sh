#!/bin/bash
# Linux/Mac installation script for Audio Transcription System

set -e  # Exit on error

echo "======================================"
echo "Audio Transcription System - Setup"
echo "======================================"
echo ""

echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi
python3 --version
echo ""

echo "[2/5] Creating virtual environment..."
cd backend
python3 -m venv venv
echo "Virtual environment created successfully"
echo ""

echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo ""

echo "[4/5] Installing dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt
echo ""

echo "[5/5] Setup environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from .env.example"
else
    echo ".env file already exists"
fi
echo ""

echo "======================================"
echo "Setup completed successfully!"
echo "======================================"
echo ""
echo "To start the backend server:"
echo "  1. cd backend"
echo "  2. source venv/bin/activate"
echo "  3. python run.py"
echo ""
echo "To start the frontend:"
echo "  1. Open new terminal"
echo "  2. cd frontend"
echo "  3. python3 -m http.server 8080"
echo ""
echo "Then open: http://localhost:8080"
echo "======================================"
