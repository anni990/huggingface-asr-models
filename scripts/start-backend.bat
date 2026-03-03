@echo off
REM Start backend server
echo Starting Audio Transcription Backend...
cd backend
call venv\Scripts\activate.bat
python run.py
