#!/bin/bash
# Production-Ready Diarization - Installation Script for Linux/Mac

echo "========================================"
echo " Universal Diarization Setup"
echo "========================================"
echo

echo "Step 1: Checking Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "[ERROR] Python not found! Please install Python 3.9+ first."
    exit 1
fi

echo
echo "Step 2: Navigating to backend directory..."
cd backend || {
    echo "[ERROR] Backend directory not found!"
    exit 1
}

echo
echo "Step 3: Setting up virtual environment..."
if [ -d "venv" ]; then
    echo "[INFO] Virtual environment exists, activating..."
    source venv/bin/activate
else
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

echo
echo "Step 4: Upgrading pip..."
python -m pip install --upgrade pip

echo
echo "Step 5: Installing dependencies (including pyannote.audio)..."
echo "[INFO] This may take a few minutes..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Failed to install dependencies!"
    echo "[INFO] You may need to install some system dependencies first:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-dev libsndfile1"
    echo "  Fedora/RHEL: sudo dnf install python3-devel libsndfile"
    echo "  macOS: brew install libsndfile"
    exit 1
fi

echo
echo "========================================"
echo " Installation Complete!"
echo "========================================"
echo
echo "Next steps:"
echo
echo "1. Get HuggingFace token:"
echo "   - Visit: https://huggingface.co/settings/tokens"
echo "   - Create a token (read access)"
echo "   - Accept license: https://huggingface.co/pyannote/speaker-diarization-3.1"
echo
echo "2. Start the backend:"
echo "   python run.py"
echo
echo "3. Test diarization:"
echo "   See DIARIZATION_GUIDE.md for usage examples"
echo
echo "========================================"
