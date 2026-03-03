"""Model capability detection service."""

from typing import Dict, Optional
from app.core.logging import get_logger

logger = get_logger(__name__)


class ModelCapabilityDetector:
    """Detect capabilities of HuggingFace models."""
    
    # Known model patterns and their capabilities
    # Note: Diarization is now universal via pyannote/speaker-diarization-3.1
    MODEL_PATTERNS = {
        "whisper": {
            "type": "whisper",
            "supports_timestamps": True,
            "processor_type": "WhisperProcessor",
            "task": "automatic-speech-recognition"
        },
        "wav2vec2": {
            "type": "wav2vec2",
            "supports_timestamps": False,
            "processor_type": "Wav2Vec2Processor",
            "task": "automatic-speech-recognition"
        },
        "qwen": {
            "type": "qwen",
            "supports_timestamps": False,
            "processor_type": "Qwen2AudioProcessor",
            "task": "audio-text-to-text"
        },
        "hubert": {
            "type": "hubert",
            "supports_timestamps": False,
            "processor_type": "Wav2Vec2Processor",
            "task": "automatic-speech-recognition"
        },
        "seamless": {
            "type": "seamless",
            "supports_timestamps": False,
            "processor_type": "AutoProcessor",
            "task": "automatic-speech-recognition"
        }
    }
    
    @classmethod
    def detect_model_type(cls, model_id: str) -> str:
        """
        Detect model type from model ID.
        
        Args:
            model_id: HuggingFace model identifier
            
        Returns:
            Model type string
        """
        model_id_lower = model_id.lower()
        
        for pattern, info in cls.MODEL_PATTERNS.items():
            if pattern in model_id_lower:
                logger.info(f"Detected model type '{info['type']}' for {model_id}")
                return info["type"]
        
        # Default to generic ASR
        logger.info(f"Unknown model type for {model_id}, using generic ASR")
        return "generic"
    
    @classmethod
    def get_model_capabilities(cls, model_id: str) -> Dict:
        """
        Get capabilities for a model.
        
        Note: Diarization is universally available via pyannote/speaker-diarization-3.1
        and is not model-specific anymore.
        
        Args:
            model_id: HuggingFace model identifier
            
        Returns:
            Dictionary of model capabilities
        """
        model_id_lower = model_id.lower()
        
        # Check known patterns
        for pattern, info in cls.MODEL_PATTERNS.items():
            if pattern in model_id_lower:
                return {
                    "model_id": model_id,
                    "model_type": info["type"],
                    "supports_timestamps": info["supports_timestamps"],
                    "supports_diarization": True,  # Universal via pyannote
                    "diarization_method": "pyannote",
                    "processor_type": info["processor_type"],
                    "task": info["task"]
                }
        
        # Default capabilities for unknown models
        return {
            "model_id": model_id,
            "model_type": "generic",
            "supports_timestamps": False,
            "supports_diarization": True,  # Universal via pyannote
            "diarization_method": "pyannote",
            "processor_type": "AutoProcessor",
            "task": "automatic-speech-recognition"
        }
    
    @classmethod
    def supports_diarization(cls, model_id: str) -> bool:
        """
        Check if model supports speaker diarization.
        
        Note: All models support diarization via pyannote/speaker-diarization-3.1
        
        Args:
            model_id: HuggingFace model identifier
            
        Returns:
            Always True (diarization is universal via pyannote)
        """
        return True  # Diarization is universal via pyannote
    
    @classmethod
    def supports_timestamps(cls, model_id: str) -> bool:
        """
        Check if model supports timestamps.
        
        Args:
            model_id: HuggingFace model identifier
            
        Returns:
            True if model supports timestamps
        """
        capabilities = cls.get_model_capabilities(model_id)
        return capabilities["supports_timestamps"]


# Global detector instance
model_detector = ModelCapabilityDetector()
