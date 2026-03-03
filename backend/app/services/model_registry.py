"""Model registry for managing and persisting loaded models."""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from app.core.logging import get_logger

logger = get_logger(__name__)


class ModelRegistry:
    """Manages model registry with JSON persistence."""
    
    def __init__(self, registry_file: str = "models_registry.json"):
        """Initialize model registry."""
        self.registry_file = Path(registry_file)
        self.models: Dict[str, Dict] = {}
        self._load_registry()
    
    def _load_registry(self) -> None:
        """Load registry from JSON file."""
        try:
            if self.registry_file.exists():
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                    self.models = data.get('models', {})
                logger.info(f"Loaded {len(self.models)} models from registry")
            else:
                logger.info("No existing registry found, starting fresh")
                self._save_registry()
        except Exception as e:
            logger.error(f"Error loading registry: {str(e)}")
            self.models = {}
    
    def _save_registry(self) -> None:
        """Save registry to JSON file."""
        try:
            data = {
                'models': self.models,
                'last_updated': datetime.utcnow().isoformat()
            }
            with open(self.registry_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved registry with {len(self.models)} models")
        except Exception as e:
            logger.error(f"Error saving registry: {str(e)}")
    
    def add_model(self, model_id: str, model_type: str = "audio") -> bool:
        """
        Add a model to the registry.
        
        Args:
            model_id: HuggingFace model identifier
            model_type: Type of model (auto-detected if not specified)
            
        Returns:
            True if added successfully
        """
        try:
            if model_id not in self.models:
                self.models[model_id] = {
                    'model_id': model_id,
                    'model_type': model_type,
                    'added_at': datetime.utcnow().isoformat(),
                    'is_loaded': False,
                    'last_used': None
                }
                self._save_registry()
                logger.info(f"Added model to registry: {model_id}")
                return True
            else:
                logger.info(f"Model already in registry: {model_id}")
                return True
        except Exception as e:
            logger.error(f"Error adding model to registry: {str(e)}")
            return False
    
    def remove_model(self, model_id: str) -> bool:
        """
        Remove a model from the registry.
        
        Args:
            model_id: HuggingFace model identifier
            
        Returns:
            True if removed successfully
        """
        try:
            if model_id in self.models:
                del self.models[model_id]
                self._save_registry()
                logger.info(f"Removed model from registry: {model_id}")
                return True
            else:
                logger.warning(f"Model not found in registry: {model_id}")
                return False
        except Exception as e:
            logger.error(f"Error removing model from registry: {str(e)}")
            return False
    
    def update_model_status(self, model_id: str, is_loaded: bool) -> None:
        """Update model loaded status."""
        if model_id in self.models:
            self.models[model_id]['is_loaded'] = is_loaded
            if is_loaded:
                self.models[model_id]['last_used'] = datetime.utcnow().isoformat()
            self._save_registry()
    
    def get_model_info(self, model_id: str) -> Optional[Dict]:
        """Get information about a specific model."""
        return self.models.get(model_id)
    
    def list_all_models(self) -> List[Dict]:
        """List all models in registry."""
        return list(self.models.values())
    
    def list_loaded_models(self) -> List[Dict]:
        """List only loaded models."""
        return [m for m in self.models.values() if m.get('is_loaded', False)]
    
    def get_recommended_models(self) -> List[str]:
        """Get list of recommended models for suggestions."""
        # These are well-tested, reliable models
        return [
            "openai/whisper-base",
            "openai/whisper-small",
            "openai/whisper-medium",
            "openai/whisper-large-v3",
            "facebook/wav2vec2-large-960h-lv60-self",
        ]


# Global registry instance
model_registry = ModelRegistry()
