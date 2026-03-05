"""Model loader and manager for HuggingFace models."""

import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, AutoModel
from typing import Optional, Dict, Any
import gc
from app.core.logging import get_logger
from app.core.config import get_settings
from app.services.model_registry import model_registry

logger = get_logger(__name__)
settings = get_settings()


class ModelManager:
    """Manages loading and caching of HuggingFace models."""
    
    def __init__(self):
        """Initialize model manager."""
        self.models: Dict[str, Any] = {}
        self.processors: Dict[str, Any] = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Model Manager initialized. Using device: {self.device}")
    
    async def load_model(self, model_id: str) -> bool:
        """
        Load a model and its processor.
        
        Args:
            model_id: HuggingFace model identifier
            
        Returns:
            bool: True if loaded successfully
        """
        try:
            if model_id in self.models:
                logger.info(f"Model {model_id} already loaded")
                return True
            
            token = settings.HUGGINGFACE_TOKEN

            logger.info(f"Loading model: {model_id}")
            
            if token:
                logger.info(f"Using HuggingFace token for authentication")
            else:
                logger.warning(f"No HuggingFace token provided. Loading may fail for private models.")

            if "indic-conformer" in model_id.lower():
                # This model doesn't use a standard AutoProcessor
                processor = None 
                model = AutoModel.from_pretrained(
                    model_id,
                    trust_remote_code=True,
                    token=token if token else None
                )
            else:
                # Standard path for Whisper/Qwen etc.
                processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, token=token)
            
            # Load model with appropriate settings
            if "Qwen2-Audio" in model_id or "Qwen3-ASR" in model_id or "Qwen" in model_id:
                # Qwen models require trust_remote_code and use AutoModel
                model = AutoModel.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    trust_remote_code=True,
                    token=token if token else None
                )
            else:
                # Standard ASR models like Whisper
                model = AutoModelForSpeechSeq2Seq.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    trust_remote_code=True,
                    token=token if token else None
                )
            
            if self.device == "cpu":
                model = model.to(self.device)
            
            self.models[model_id] = model
            self.processors[model_id] = processor
            
            # Update registry
            model_type = "whisper" if "whisper" in model_id.lower() else "other"
            model_registry.add_model(model_id, model_type)
            model_registry.update_model_status(model_id, True)
            
            logger.info(f"Successfully loaded model: {model_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model {model_id}: {str(e)}")
            return False
    
    def get_model(self, model_id: str) -> Optional[Any]:
        """Get a loaded model."""
        return self.models.get(model_id)
    
    def get_processor(self, model_id: str) -> Optional[Any]:
        """Get a loaded processor."""
        return self.processors.get(model_id)
    
    def is_model_loaded(self, model_id: str) -> bool:
        """Check if a model is loaded."""
        return model_id in self.models
    
    def unload_model(self, model_id: str) -> bool:
        """
        Unload a model to free memory.
        
        Args:
            model_id: Model identifier to unload
            
        Returns:
            bool: True if unloaded successfully
        """
        try:
            if model_id in self.models:
                del self.models[model_id]
                del self.processors[model_id]
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                # Update registry
                model_registry.update_model_status(model_id, False)
                
                logger.info(f"Unloaded model: {model_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error unloading model {model_id}: {str(e)}")
            return False
    
    def get_loaded_models(self) -> list:
        """Get list of loaded model IDs."""
        return list(self.models.keys())


# Global model manager instance
model_manager = ModelManager()
