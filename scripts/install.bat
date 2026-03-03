@echo off
REM Windows installation script for Audio Transcription System
echo ======================================
echo Audio Transcription System - Setup
echo ======================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

echo [2/5] Creating virtual environment...
cd backend
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [4/5] Installing dependencies...
echo This may take several minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [5/5] Setup environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example
) else (
    echo .env file already exists
)
echo.

echo ======================================
echo Setup completed successfully!
echo ======================================
echo.
echo To start the backend server:
echo   1. cd backend
echo   2. venv\Scripts\activate
echo   3. python run.py
echo.
echo To start the frontend:
echo   1. Open new terminal
echo   2. cd frontend
echo   3. python -m http.server 8080
echo.
echo Then open: http://localhost:8080
echo ======================================
pause
