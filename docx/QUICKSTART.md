# Quick Start Guide

This guide will help you get the Audio Transcription System up and running quickly.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9 or higher (`python --version`)
- ✅ pip installed (`pip --version`)
- ✅ Modern web browser (Chrome, Firefox, Safari, Edge)

## Step-by-Step Setup

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies (this may take a few minutes)
pip install -r requirements.txt

# Environment is already created (.env file)
# You can edit it to change settings

# Start the backend server
python run.py
```

**Expected output:**
```
INFO - Starting HuggingFace Audio Transcription API...
INFO - Default model: Qwen/Qwen2-Audio-7B-Instruct
INFO - Pre-loading default model...
INFO - Model Manager initialized. Using device: cuda/cpu
INFO - Loading model: Qwen/Qwen2-Audio-7B-Instruct
```

The first time you run, it will download the model (may take several minutes depending on your internet speed).

**Server will be available at:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 2. Frontend Setup (1 minute)

Open a **new terminal** (keep backend running):

```bash
# Navigate to frontend folder
cd frontend

# Start simple HTTP server
python -m http.server 8080
```

**Open in browser:**
http://localhost:8080

## Quick Test

1. Open http://localhost:8080 in your browser
2. Check that the status badge shows "Online" (green)
3. Prepare a test audio file (WAV, MP3, or other supported format)
4. Drag and drop the file onto the upload area
5. Click "Transcribe"
6. Wait for results (processing time depends on file length and hardware)

## Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`
- **Solution:** Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

**Error:** `Port 8000 already in use`
- **Solution:** Change PORT in `.env` file or stop other services using port 8000

### Frontend shows "API is offline"

- **Solution:** Ensure backend is running at http://localhost:8000
- **Test:** Open http://localhost:8000/health in browser

### Model download is slow

- **Normal:** First-time model download can take 5-15 minutes depending on internet speed
- **Models are large:** Qwen2-Audio-7B is several GB

### Out of memory error

- **Solution 1:** Use a smaller model (edit DEFAULT_MODEL in `.env`):
  ```env
  DEFAULT_MODEL=openai/whisper-small
  ```
- **Solution 2:** Close other applications to free memory

## Next Steps

✅ **Explore API Documentation:** http://localhost:8000/docs

✅ **Try Different Models:** Edit `DEFAULT_MODEL` in `backend/.env`

✅ **Test API Directly:**
```bash
curl -X POST "http://localhost:8000/api/v1/transcription/transcribe" \
  -F "file=@your_audio.wav"
```

✅ **Read Full Documentation:** See main README.md

## Common Configuration Changes

### Change Server Port
Edit `backend/.env`:
```env
PORT=8080
```

### Change Max File Size
Edit `backend/.env`:
```env
MAX_AUDIO_SIZE_MB=50
```

### Use Different Model
Edit `backend/.env`:
```env
DEFAULT_MODEL=openai/whisper-large-v3
```

### Update CORS for Different Frontend Port
Edit `backend/.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Stopping the Services

### Stop Backend
Press `Ctrl+C` in the backend terminal

### Stop Frontend
Press `Ctrl+C` in the frontend terminal

### Deactivate Virtual Environment
```bash
deactivate
```

## Getting Help

- Check `/docs` endpoint for API documentation
- Review error logs in terminal
- See main README.md for detailed information
- Check individual service READMEs in `backend/` and `frontend/`

---

**Congratulations!** 🎉 You now have a working audio transcription system!
