@echo off
REM Production-Ready Diarization - Installation Script for Windows

echo ========================================
echo  Universal Diarization Setup
echo ========================================
echo.

echo Step 1: Checking Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.9+ first.
    pause
    exit /b 1
)

echo.
echo Step 2: Navigating to backend directory...
cd backend
if errorlevel 1 (
    echo [ERROR] Backend directory not found!
    pause
    exit /b 1
)

echo.
echo Step 3: Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate
    echo [OK] Virtual environment activated
) else (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo [OK] Virtual environment created and activated
)

echo.
echo Step 4: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 5: Installing dependencies (including pyannote.audio)...
echo [INFO] This may take a few minutes...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo [INFO] You may need to install some system dependencies first.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Get HuggingFace token:
echo    - Visit: https://huggingface.co/settings/tokens
echo    - Create a token (read access)
echo    - Accept license: https://huggingface.co/pyannote/speaker-diarization-3.1
echo.
echo 2. Start the backend:
echo    python run.py
echo.
echo 3. Test diarization:
echo    See DIARIZATION_GUIDE.md for usage examples
echo.
echo ========================================
pause
