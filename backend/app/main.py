"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.api.routes import transcription
from app.models.schemas import HealthResponse
from app.services.model_loader import model_manager
from app.utils.file_handler import file_handler

# Setup logging
setup_logging()
logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info("Starting HuggingFace Audio Transcription API...")
    logger.info(f"Default model: {settings.DEFAULT_MODEL}")
    
    # Pre-load models from configuration
    preload_models = settings.preload_models_list
    logger.info(f"Pre-loading {len(preload_models)} models: {', '.join(preload_models)}")
    
    for model_id in preload_models:
        try:
            logger.info(f"Loading model: {model_id}")
            await model_manager.load_model(model_id)
            logger.info(f"✓ Loaded: {model_id}")
        except Exception as e:
            logger.error(f"✗ Failed to load {model_id}: {str(e)}")
    
    # Cleanup old files on startup
    await file_handler.cleanup_old_files()
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Generic Audio Transcription API with Speaker Diarization
    
    **Universal HuggingFace Model Support** - Load and use ANY speech recognition model from HuggingFace.
    
    ### Key Features:
    * 🎯 **Generic Model Support** - Works with Whisper, Wav2Vec2, Hubert, Qwen, and any HuggingFace ASR model
    * 🗣️ **Speaker Diarization** - Identify different speakers in audio (Whisper models)
    * ⚡ **Auto-Detection** - Automatically detects model capabilities
    * 🔄 **Fallback Mechanisms** - Graceful degradation for unsupported features
    * 📦 **Model Management** - Load, unload, and manage multiple models
    * 🚀 **Production Ready** - Built for integration with any backend or frontend
    
    ### Supported Model Types:
    * OpenAI Whisper (all sizes) - **Recommended for diarization**
    * Meta Wav2Vec2 / HuBERT
    * Alibaba Qwen2-Audio
    * Facebook Seamless M4T
    * Any HuggingFace automatic-speech-recognition model
    
    ### Quick Start:
    1. Load a model: `POST /api/v1/transcription/models/load`
    2. Transcribe audio: `POST /api/v1/transcription/transcribe`
    3. Check capabilities: `GET /api/v1/transcription/models/capabilities/{model_id}`
    
    ### API Integration:
    All endpoints return standardized JSON responses for easy integration.
    Use `/docs` for interactive API testing with Swagger UI.
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcription.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "HuggingFace Audio Transcription API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        models_loaded=len(model_manager.get_loaded_models())
    )


@app.get("/debug/cors", tags=["Debug"])
async def debug_cors():
    """Debug CORS configuration."""
    return {
        "cors_origins": settings.cors_origins_list,
        "total_origins": len(settings.cors_origins_list),
        "includes_5173": "http://localhost:5173" in settings.cors_origins_list,
        "includes_5174": "http://localhost:5174" in settings.cors_origins_list,
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
