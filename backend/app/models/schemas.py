"""Request and response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class DiarizationSegment(BaseModel):
    """Diarization segment model."""
    
    channel: int = Field(..., description="Speaker channel/ID")
    offset: float = Field(..., description="Start time in seconds")
    duration: float = Field(..., description="Duration in seconds")
    text: str = Field(..., description="Transcribed text for this segment")
    
    class Config:
        json_schema_extra = {
            "example": {
                "channel": 0,
                "offset": 14.92,
                "duration": 0.36,
                "text": "Hello."
            }
        }


class TranscriptionResponse(BaseModel):
    """Transcription response model."""
    
    success: bool = Field(..., description="Whether the transcription was successful")
    transcription: Optional[str] = Field(None, description="The transcribed text")
    model_used: str = Field(..., description="The model used for transcription")
    audio_duration: Optional[float] = Field(None, description="Audio duration in seconds")
    processing_time: float = Field(..., description="Processing time in seconds")
    diarization: Optional[List[DiarizationSegment]] = Field(None, description="Speaker diarization data")
    diarization_enabled: bool = Field(False, description="Whether diarization was requested")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    error: Optional[str] = Field(None, description="Error message if any")
    
    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "success": True,
                "transcription": "Hello, this is a sample transcription.",
                "model_used": "Qwen/Qwen2-Audio-7B-Instruct",
                "audio_duration": 5.2,
                "processing_time": 1.3,
                "diarization": [
                    {"channel": 0, "offset": 0.0, "duration": 2.5, "text": "Hello there."},
                    {"channel": 1, "offset": 2.5, "duration": 3.0, "text": "Hi, how are you?"}
                ],
                "diarization_enabled": True,
                "timestamp": "2024-01-01T12:00:00",
                "error": None
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    success: bool = False
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Invalid audio format",
                "details": {"allowed_formats": [".wav", ".mp3", ".flac"]},
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    models_loaded: int = Field(..., description="Number of models loaded")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ModelInfo(BaseModel):
    """Model information schema."""
    
    model_id: str = Field(..., description="HuggingFace model ID")
    is_loaded: bool = Field(..., description="Whether the model is currently loaded")
    model_type: str = Field(default="audio", description="Type of model")
    supports_diarization: bool = Field(default=False, description="Whether model supports diarization")
    
    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "model_id": "Qwen/Qwen2-Audio-7B-Instruct",
                "is_loaded": True,
                "model_type": "audio"
            }
        }
