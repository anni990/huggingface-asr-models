@echo off
REM Start React + Vite frontend server
echo Starting Audio Transcription Frontend (React + Vite)...
echo.
echo Installing dependencies if needed...
cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing npm packages...
    call npm install
)

echo.
echo Starting development server...
echo Frontend will be available at: http://localhost:5173
echo Press Ctrl+C to stop the server
echo.
call npm run dev
