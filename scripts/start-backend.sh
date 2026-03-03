#!/bin/bash
# Start backend server
echo "Starting Audio Transcription Backend..."
cd backend
source venv/bin/activate
python run.py
