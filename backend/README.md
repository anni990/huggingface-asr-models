# Audio Transcription API - Backend

Production-ready FastAPI backend for audio transcription using HuggingFace models.

## Features

- 🎯 **Multi-Model Support**: Easily switch between different HuggingFace ASR models
- 🚀 **Async Processing**: Fast, non-blocking audio transcription
- 📦 **Modular Architecture**: Clean separation of concerns for easy maintenance
- 🔒 **Input Validation**: File type and size validation
- 📊 **Comprehensive Logging**: Detailed logging for debugging and monitoring
- 🔄 **Auto Model Loading**: Models are loaded on-demand or pre-loaded on startup
- 🌐 **CORS Support**: Ready for frontend integration
- 📝 **OpenAPI Documentation**: Interactive API docs at `/docs`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── transcription.py   # Transcription endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   └── logging.py             # Logging setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_loader.py        # Model management
│   │   └── transcription_service.py
│   └── utils/
│       ├── __init__.py
│       └── file_handler.py        # File operations
├── requirements.txt
├── .env.example
├── .gitignore
├── run.py                         # Application runner
└── README.md
```

## Installation

### Prerequisites

- Python 3.9+
- CUDA-compatible GPU (optional, for faster processing)

### Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` to customize settings:
   ```env
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   DEFAULT_MODEL=Qwen/Qwen2-Audio-7B-Instruct
   MAX_AUDIO_SIZE_MB=25
   ```

## Usage

### Start the Server

```bash
# Using run.py
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```http
GET /health
```

### Transcribe Audio
```http
POST /api/v1/transcription/transcribe
Content-Type: multipart/form-data

file: <audio_file>
model_id: <optional_model_id>
```

**Example using cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/transcription/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav"
```

**Example with custom model**:
```bash
curl -X POST "http://localhost:8000/api/v1/transcription/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav" \
  -F "model_id=Qwen/Qwen2-Audio-7B-Instruct"
```

### List Loaded Models
```http
GET /api/v1/transcription/models
```

### Load Model
```http
POST /api/v1/transcription/models/load
Content-Type: multipart/form-data

model_id: <model_id>
```

### Unload Model
```http
DELETE /api/v1/transcription/models/{model_id}/unload
```

## Supported Models

The API supports various HuggingFace ASR models:

- `Qwen/Qwen2-Audio-7B-Instruct` (default)
- `Qwen/Qwen3-ASR-1.7B`
- `openai/whisper-large-v3`
- `openai/whisper-medium`
- Any other compatible HuggingFace ASR model

## Supported Audio Formats

- WAV (.wav)
- MP3 (.mp3)
- FLAC (.flac)
- M4A (.m4a)
- OGG (.ogg)

**Maximum file size**: 25 MB (configurable)

## Configuration

Configure the application via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `DEBUG` | Debug mode | True |
| `DEFAULT_MODEL` | Default HuggingFace model | Qwen/Qwen2-Audio-7B-Instruct |
| `MAX_AUDIO_SIZE_MB` | Max upload size in MB | 25 |
| `ALLOWED_AUDIO_FORMATS` | Allowed file extensions | .wav,.mp3,.flac,.m4a,.ogg |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000,... |
| `LOG_LEVEL` | Logging level | INFO |

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
```

### Linting
```bash
flake8 app/
```

## Deployment

### Docker Deployment (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
```

Build and run:
```bash
docker build -t transcription-api .
docker run -p 8000:8000 transcription-api
```

### Production Settings

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a production ASGI server (uvicorn with gunicorn)
3. Set up SSL/TLS
4. Configure proper CORS origins
5. Set up monitoring and logging

## Performance Optimization

### GPU Acceleration
The API automatically uses CUDA if available. Ensure you have:
- CUDA-compatible GPU
- CUDA toolkit installed
- PyTorch with CUDA support

### Model Caching
Models are cached in memory after first load. For faster startup:
- Pre-load models on application startup
- Use model warmup endpoints before handling requests

## Troubleshooting

### Model Loading Issues
```bash
# Clear HuggingFace cache
rm -rf ~/.cache/huggingface/
```

### Out of Memory
- Reduce model size (use smaller variants)
- Limit concurrent requests
- Increase system memory or use GPU

### Audio Format Issues
- Ensure ffmpeg is installed for audio conversion
- Check file format compatibility

## License

MIT License

## Support

For issues and questions:
- Check the [API documentation](http://localhost:8000/docs)
- Review logs for error details
- Check HuggingFace model documentation
