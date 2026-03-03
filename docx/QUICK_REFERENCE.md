# 🚀 Quick Reference - Universal Audio Transcription Platform

## 📋 Essential Commands

### Start the Application
```bash
# Windows
.\run.bat

# Linux/Mac
./run.sh

# Or start separately:
.\start-backend.bat    # Start backend only
.\start-frontend.bat   # Start frontend only
```

### Access Points
- **Frontend UI**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health

---

## 🎯 Key Endpoints

```bash
# Health check
GET http://localhost:8000/health

# Get model capabilities (NEW!)
GET http://localhost:8000/api/v1/transcription/models/capabilities/{model_id}

# List all models with capabilities
GET http://localhost:8000/api/v1/transcription/models/registry

# Load a model
POST http://localhost:8000/api/v1/transcription/models/load
Content-Type: multipart/form-data
model_id=openai/whisper-base

# Transcribe with diarization
POST http://localhost:8000/api/v1/transcription/transcribe
Content-Type: multipart/form-data
file=@audio.mp3
model_id=openai/whisper-base
diarization=true
```

---

## 🧪 Quick Test

```bash
# 1. Test the platform
python test_generic_platform.py

# 2. Manual curl test
curl http://localhost:8000/health

# 3. Check capabilities of a model
curl "http://localhost:8000/api/v1/transcription/models/capabilities/openai/whisper-tiny"
```

---

## 📦 Supported Models

### ⭐ Recommended for Testing
```
openai/whisper-tiny       # 39M - Ultra-fast
openai/whisper-base       # 74M - Good balance
```

### 🚀 Production Models
```
openai/whisper-small      # 244M - Good accuracy
openai/whisper-medium     # 769M - High accuracy
openai/whisper-large-v3   # 1550M - Best accuracy
```

### 🌍 Other Model Types
```
facebook/wav2vec2-base-960h              # Fast, English-only
facebook/wav2vec2-large-960h-lv60-self   # Better accuracy
Qwen/Qwen2-Audio-7B-Instruct            # Multi-task audio
facebook/hubert-large-ls960-ft           # Alternative ASR
```

---

## 🎨 Frontend Features

### Model Selection
1. Go to "Model Management" tab
2. Enter HuggingFace model ID
3. Click "Load Model"
4. Wait for loading (progress shown)

### Transcription
1. Go to "Transcribe" tab
2. Select loaded model
3. Check capabilities (auto-displayed)
4. Toggle diarization if supported
5. Upload audio file (drag & drop)
6. Click "Transcribe"

### View Results
- **Transcription text** with copy button
- **Speaker segments** (if diarization enabled)
- **JSON response** (toggle to view)
- **Processing metrics** (duration, time)

---

## 🔍 Capability Badges

When you select a model, you'll see:
- **⏱️ Timestamps** - Model provides timing info
- **👥 Diarization** - Model supports speaker identification
- **Type: whisper** - Model type detected

---

## 📊 API Response Format

```json
{
  "success": true,
  "transcription": "Full text here...",
  "model_used": "openai/whisper-base",
  "audio_duration": 45.2,
  "processing_time": 3.5,
  "diarization_enabled": true,
  "diarization": [
    {
      "channel": 0,
      "offset": 0.0,
      "duration": 2.5,
      "text": "Speaker 1 speaking..."
    },
    {
      "channel": 1,
      "offset": 2.5,
      "duration": 3.0,
      "text": "Speaker 2 responding..."
    }
  ],
  "timestamp": "2026-03-03T12:00:00"
}
```

---

## 🐍 Python Integration

```python
import requests

# Load model
requests.post(
    "http://localhost:8000/api/v1/transcription/models/load",
    data={"model_id": "openai/whisper-base"},
    timeout=300
)

# Check capabilities
caps = requests.get(
    "http://localhost:8000/api/v1/transcription/models/capabilities/openai/whisper-base"
).json()

print(f"Diarization: {caps['capabilities']['supports_diarization']}")

# Transcribe
with open("audio.mp3", "rb") as f:
    result = requests.post(
        "http://localhost:8000/api/v1/transcription/transcribe",
        files={"file": f},
        data={"model_id": "openai/whisper-base", "diarization": True},
        timeout=600
    ).json()

print(result["transcription"])
for seg in result["diarization"]:
    print(f"Speaker {seg['channel']}: {seg['text']}")
```

---

## 🔧 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Activate venv and reinstall
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 16+

# Reinstall dependencies
cd frontend
npm install
```

### Model loading fails
- **First load**: Model downloads from HuggingFace (takes time)
- **Out of memory**: Try smaller model (whisper-tiny/base)
- **Network issue**: Check internet connection

### Transcription timeout
- **File too large**: Max 25MB, or reduce audio length
- **Model too slow**: Use smaller/faster model
- **System resources**: Close other applications

---

## 📚 Documentation Files

- **README.md** - Main project documentation
- **API_INTEGRATION_GUIDE.md** - Complete API integration guide
- **GENERIC_PLATFORM_SUMMARY.md** - Implementation summary
- **PROJECT_SUMMARY.md** - Architecture overview
- **QUICKSTART.md** - Quick setup guide

---

## 💡 Pro Tips

1. **Start with whisper-tiny** for testing (fastest)
2. **Check capabilities** before enabling diarization
3. **Use drag & drop** for file upload (no double-click!)
4. **Toggle JSON view** to see complete API response
5. **Copy diarization** to get formatted speaker segments

---

## ⚙️ Configuration

### Backend `.env`
```env
DEFAULT_MODEL=openai/whisper-base
MAX_AUDIO_SIZE_MB=25
ALLOWED_AUDIO_FORMATS=.wav,.mp3,.flac,.m4a,.ogg
PORT=8000
```

### Frontend `api.js`
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

---

## 🎯 What Makes This "Generic"?

✅ Works with **ANY** HuggingFace ASR model  
✅ **Auto-detects** model type and capabilities  
✅ **No hardcoded** model lists  
✅ **Graceful fallbacks** for unsupported features  
✅ **Universal API** - same endpoints for all models  
✅ **Easy integration** - just provide model ID  

---

## 🆘 Getting Help

1. Check **API docs**: http://localhost:8000/docs
2. Read **API_INTEGRATION_GUIDE.md**
3. Review **error messages** in UI or console
4. Check **browser console** (F12) for frontend issues
5. Check **backend logs** in terminal

---

**For detailed information, see:**
- 📖 [README.md](README.md)
- 🔗 [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md)
- 📋 [GENERIC_PLATFORM_SUMMARY.md](GENERIC_PLATFORM_SUMMARY.md)

---

**Happy Transcribing! 🎙️✨**
