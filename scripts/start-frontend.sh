#!/bin/bash
# Start React + Vite frontend server
echo "Starting Audio Transcription Frontend (React + Vite)..."
echo ""
echo "Installing dependencies if needed..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
fi

echo ""
echo "Starting development server..."
echo "Frontend will be available at: http://localhost:5173"
echo "Press Ctrl+C to stop the server"
echo ""
npm run dev
