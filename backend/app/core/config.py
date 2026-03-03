"""Application configuration management."""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    
    # Model Configuration
    DEFAULT_MODEL: str = "openai/whisper-base"
    PRELOAD_MODELS: str = "openai/whisper-base,openai/whisper-small"
    MAX_AUDIO_SIZE_MB: int = 25
    ALLOWED_AUDIO_FORMATS: str = ".wav,.mp3,.flac,.m4a,.ogg"
    
    # HuggingFace Configuration
    HUGGINGFACE_TOKEN: str = ""  # Required for pyannote diarization
    
    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:5174,http://localhost:8080,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:5500"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Application
    APP_NAME: str = "HuggingFace Audio Transcription API"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def allowed_formats_list(self) -> List[str]:
        """Get allowed audio formats as a list."""
        return [fmt.strip() for fmt in self.ALLOWED_AUDIO_FORMATS.split(",")]
    
    @property
    def preload_models_list(self) -> List[str]:
        """Get preload models as a list."""
        return [model.strip() for model in self.PRELOAD_MODELS.split(",") if model.strip()]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def max_audio_size_bytes(self) -> int:
        """Get max audio size in bytes."""
        return self.MAX_AUDIO_SIZE_MB * 1024 * 1024


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
