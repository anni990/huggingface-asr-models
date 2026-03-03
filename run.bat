@echo off
echo Starting Audio Transcription Project...
echo.
echo [1/2] Starting Frontend (React + Vite)...
REM Start Frontend in new terminal
start cmd /k "echo === Frontend Server === && cd frontend && npm run dev"

echo [2/2] Starting Backend (FastAPI)...
REM Start Backend in new terminal
start cmd /k "echo === Backend Server === && cd backend && call venv\Scripts\activate.bat && python run.py"

echo.
echo ================================================
echo Both servers are starting in separate terminals
echo ================================================
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ================================================