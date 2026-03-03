# Audio Transcription API - Integration Guide

## 🚀 Overview

This is a **universal, production-ready Audio Transcription API** that supports ANY HuggingFace speech recognition model with automatic capability detection, speaker diarization, and fallback mechanisms.

## 🎯 Key Features

- **Universal Model Support**: Load and use ANY HuggingFace ASR model
- **Auto-Detection**: Automatically detects model capabilities (diarization, timestamps)
- **Speaker Diarization**: Identify different speakers in multi-speaker audio
- **Fallback Mechanisms**: Gracefully handles unsupported features
- **Production Ready**: Built for easy integration with any backend or frontend

---

## 📋 API Endpoints

### Base URL
```
http://localhost:8000/api/v1/transcription
```

### 1. **Transcribe Audio** 
`POST /transcribe`

Upload an audio file and get transcription with optional speaker diarization.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/transcription/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.mp3" \
  -F "model_id=openai/whisper-base" \
  -F "diarization=true"
```

**Parameters:**
- `file` (required): Audio file (.wav, .mp3, .flac, .m4a, .ogg)
- `model_id` (optional): HuggingFace model ID (defaults to configured model)
- `diarization` (optional): Enable speaker diarization (default: true)

**Response:**
```json
{
  "success": true,
  "transcription": "Full transcription text here...",
  "model_used": "openai/whisper-base",
  "audio_duration": 45.2,
  "processing_time": 3.5,
  "diarization_enabled": true,
  "diarization": [
    {
      "channel": 0,
      "offset": 0.0,
      "duration": 2.5,
      "text": "Hello, how are you?"
    },
    {
      "channel": 1,
      "offset": 2.5,
      "duration": 3.0,
      "text": "I'm doing great, thanks!"
    }
  ],
  "timestamp": "2026-03-03T12:00:00"
}
```

---

### 2. **Get Model Capabilities**
`GET /models/capabilities/{model_id}`

Check what features a model supports before using it.

**Request:**
```bash
curl "http://localhost:8000/api/v1/transcription/models/capabilities/openai/whisper-base"
```

**Response:**
```json
{
  "success": true,
  "model_id": "openai/whisper-base",
  "capabilities": {
    "model_id": "openai/whisper-base",
    "model_type": "whisper",
    "supports_timestamps": true,
    "supports_diarization": true,
    "processor_type": "WhisperProcessor",
    "task": "automatic-speech-recognition"
  }
}
```

---

### 3. **Load Model**
`POST /models/load`

Load any HuggingFace speech recognition model into memory.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/transcription/models/load" \
  -H "Content-Type: multipart/form-data" \
  -F "model_id=openai/whisper-large-v3"
```

**Supported Models:**
- `openai/whisper-tiny` (39M) - Fastest
- `openai/whisper-base` (74M) - Recommended for testing
- `openai/whisper-small` (244M)
- `openai/whisper-medium` (769M)
- `openai/whisper-large-v3` (1550M) - Most accurate
- `facebook/wav2vec2-large-960h-lv60-self`
- `facebook/hubert-large-ls960-ft`
- `Qwen/Qwen2-Audio-7B-Instruct`
- **ANY HuggingFace automatic-speech-recognition model!**

**Response:**
```json
{
  "success": true,
  "message": "Model openai/whisper-large-v3 loaded successfully",
  "model_id": "openai/whisper-large-v3"
}
```

---

### 4. **List Registered Models**
`GET /models/registry`

Get all registered models with their capabilities and status.

**Request:**
```bash
curl "http://localhost:8000/api/v1/transcription/models/registry"
```

**Response:**
```json
{
  "success": true,
  "models": [
    {
      "model_id": "openai/whisper-base",
      "is_loaded": true,
      "model_type": "whisper",
      "supports_diarization": true,
      "supports_timestamps": true,
      "added_at": "2026-03-03T10:00:00",
      "last_used": "2026-03-03T12:00:00"
    }
  ],
  "total_count": 1,
  "loaded_count": 1
}
```

---

### 5. **Unload Model**
`DELETE /models/unload`

Remove a model from memory (keeps in registry).

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/transcription/models/unload" \
  -H "Content-Type: multipart/form-data" \
  -F "model_id=openai/whisper-base"
```

---

### 6. **Delete Model**
`DELETE /models/delete`

Completely remove a model from registry and memory.

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/transcription/models/delete" \
  -H "Content-Type: multipart/form-data" \
  -F "model_id=openai/whisper-base"
```

---

## 🔧 Integration Examples

### JavaScript/TypeScript (Frontend)

```javascript
// API Service
class TranscriptionAPI {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  async transcribe(audioFile, modelId = 'openai/whisper-base', enableDiarization = true) {
    const formData = new FormData();
    formData.append('file', audioFile);
    formData.append('model_id', modelId);
    formData.append('diarization', enableDiarization);

    const response = await fetch(`${this.baseURL}/api/v1/transcription/transcribe`, {
      method: 'POST',
      body: formData
    });

    return await response.json();
  }

  async getModelCapabilities(modelId) {
    const response = await fetch(
      `${this.baseURL}/api/v1/transcription/models/capabilities/${modelId}`
    );
    return await response.json();
  }

  async loadModel(modelId) {
    const formData = new FormData();
    formData.append('model_id', modelId);

    const response = await fetch(`${this.baseURL}/api/v1/transcription/models/load`, {
      method: 'POST',
      body: formData
    });

    return await response.json();
  }
}

// Usage Example
const api = new TranscriptionAPI();

// Upload and transcribe
const audioFile = document.getElementById('audioInput').files[0];
const result = await api.transcribe(audioFile, 'openai/whisper-base', true);

console.log('Transcription:', result.transcription);
console.log('Speakers:', result.diarization);
```

---

### Python (Backend Integration)

```python
import requests

class TranscriptionClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1/transcription"
    
    def transcribe(self, audio_path, model_id='openai/whisper-base', diarization=True):
        """Transcribe audio file"""
        with open(audio_path, 'rb') as f:
            files = {'file': f}
            data = {
                'model_id': model_id,
                'diarization': diarization
            }
            response = requests.post(
                f"{self.api_url}/transcribe",
                files=files,
                data=data,
                timeout=600  # 10 minutes
            )
        return response.json()
    
    def get_capabilities(self, model_id):
        """Get model capabilities"""
        response = requests.get(
            f"{self.api_url}/models/capabilities/{model_id}"
        )
        return response.json()
    
    def load_model(self, model_id):
        """Load a model"""
        response = requests.post(
            f"{self.api_url}/models/load",
            data={'model_id': model_id},
            timeout=300  # 5 minutes for loading
        )
        return response.json()

# Usage
client = TranscriptionClient()

# Load a model
client.load_model('openai/whisper-base')

# Transcribe audio
result = client.transcribe('audio.mp3', diarization=True)

print(f"Transcription: {result['transcription']}")
for segment in result.get('diarization', []):
    print(f"Speaker {segment['channel']}: {segment['text']}")
```

---

### Node.js (Express Backend)

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class TranscriptionAPI {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  async transcribe(audioPath, modelId = 'openai/whisper-base', diarization = true) {
    const formData = new FormData();
    formData.append('file', fs.createReadStream(audioPath));
    formData.append('model_id', modelId);
    formData.append('diarization', diarization);

    const response = await axios.post(
      `${this.baseURL}/api/v1/transcription/transcribe`,
      formData,
      {
        headers: formData.getHeaders(),
        timeout: 600000 // 10 minutes
      }
    );

    return response.data;
  }
}

// Usage in Express route
app.post('/api/transcribe', async (req, res) => {
  const api = new TranscriptionAPI();
  const result = await api.transcribe(req.file.path, req.body.model_id);
  res.json(result);
});
```

---

## 🎨 Best Practices

### 1. **Check Capabilities First**
```javascript
// Before using a model, check its capabilities
const caps = await api.getModelCapabilities('openai/whisper-base');
if (caps.capabilities.supports_diarization) {
  // Enable diarization
  const result = await api.transcribe(file, modelId, true);
}
```

### 2. **Handle Timeouts Properly**
```javascript
// Set appropriate timeouts for long-running operations
const result = await fetch(url, {
  timeout: 600000 // 10 minutes for transcription
});
```

### 3. **Use Fallbacks**
```javascript
// If diarization fails, you still get transcription
if (result.success) {
  const text = result.transcription;
  const speakers = result.diarization || []; // May be null/empty
}
```

### 4. **Model Selection**
- **Fast testing**: `openai/whisper-tiny` or `openai/whisper-base`
- **Production**: `openai/whisper-small` or `openai/whisper-medium`
- **Best accuracy**: `openai/whisper-large-v3`
- **Multilingual**: Most Whisper models support 90+ languages

---

## 🔍 Error Handling

All endpoints return standardized errors:

```json
{
  "detail": "Error message here"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad request (invalid file, missing parameters)
- `404`: Model not found
- `500`: Server error

**Example Error Handling:**
```javascript
try {
  const result = await api.transcribe(file, modelId);
  if (!result.success) {
    console.error('Error:', result.error);
  }
} catch (error) {
  console.error('Request failed:', error.message);
}
```

---

## 📊 Response Format

All successful responses follow this structure:

```typescript
interface TranscriptionResponse {
  success: boolean;
  transcription: string | null;
  model_used: string;
  audio_duration: number | null;
  processing_time: number;
  diarization_enabled: boolean;
  diarization: DiarizationSegment[] | null;
  timestamp: string;
  error?: string;
}

interface DiarizationSegment {
  channel: number;      // Speaker ID (0, 1, 2, ...)
  offset: number;       // Start time in seconds
  duration: number;     // Duration in seconds
  text: string;         // Transcribed text
}
```

---

## 🚀 Quick Start Checklist

1. ✅ Start the backend: `python run.py`
2. ✅ Access API docs: http://localhost:8000/docs
3. ✅ Load a model: `POST /models/load`
4. ✅ Upload audio: `POST /transcribe`
5. ✅ Get results with diarization

---

## 💡 Tips

- **Default model**: If you don't specify a model, it uses the configured default
- **Diarization**: Works best with Whisper models
- **File size**: Maximum 25MB per file
- **Formats**: WAV, MP3, FLAC, M4A, OGG supported
- **Processing time**: Varies by model size and audio length

---

## 📞 Support

- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

---

**Happy Integrating! 🎉**
