"""Transcription API routes."""

import time
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List
from app.models.schemas import TranscriptionResponse, ErrorResponse, ModelInfo
from app.services.transcription_service import transcription_service
from app.services.model_loader import model_manager
from app.services.model_registry import model_registry
from app.services.model_detector import model_detector
from app.services.diarization_service import diarization_service
from app.utils.file_handler import file_handler
from app.core.config import get_settings
from app.core.logging import get_logger

router = APIRouter(prefix="/api/v1/transcription", tags=["Transcription"])
logger = get_logger(__name__)
settings = get_settings()


@router.post(
    "/transcribe",
    response_model=TranscriptionResponse,
    summary="Transcribe audio file",
    description="Upload an audio file and get transcription using specified model"
)
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe"),
    model_id: Optional[str] = Form(
        default=None,
        description="HuggingFace model ID (defaults to configured model)"
    ),
    diarization: bool = Form(
        default=True,
        description="Enable speaker diarization (if supported by model)"
    )
):
    """
    Transcribe an audio file using HuggingFace model.
    
    Args:
        file: Audio file upload
        model_id: Optional model ID (uses default if not specified)
        diarization: Enable speaker diarization
        
    Returns:
        TranscriptionResponse with transcription results
    """
    file_path = None
    start_time = time.time()
    
    try:
        # Use default model if not specified
        model = model_id or settings.DEFAULT_MODEL
        
        logger.info(f"Transcription request: file={file.filename}, model={model}, diarization={diarization}")
        
        # Save uploaded file
        file_path = await file_handler.save_upload_file(file)
        
        # Perform transcription with optional diarization (using pyannote)
        transcription, diarization_segments, duration = await transcription_service.transcribe(
            audio_path=file_path,
            model_id=model,
            enable_diarization=diarization
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        response = TranscriptionResponse(
            success=True,
            transcription=transcription,
            model_used=model,
            audio_duration=duration,
            processing_time=processing_time,
            diarization=diarization_segments,
            diarization_enabled=diarization and diarization_segments is not None
        )
        
        logger.info(f"Transcription successful: {processing_time:.2f}s, diarization={'enabled' if diarization_segments else 'disabled'}")
        return response
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        processing_time = time.time() - start_time
        
        return TranscriptionResponse(
            success=False,
            transcription=None,
            model_used=model_id or settings.DEFAULT_MODEL,
            processing_time=processing_time,
            diarization_enabled=False,
            error=str(e)
        )
    
    finally:
        # Clean up uploaded file
        if file_path:
            await file_handler.delete_file(file_path)


@router.get(
    "/models/capabilities/{model_id:path}",
    summary="Get model capabilities",
    description="Get capabilities and features supported by a specific model"
)
async def get_model_capabilities(model_id: str):
    """
    Get capabilities of a specific model.
    
    Args:
        model_id: HuggingFace model identifier (use path format, e.g., openai/whisper-base)
        
    Returns:
        Model capabilities including diarization support, timestamps, etc.
    """
    try:
        capabilities = model_detector.get_model_capabilities(model_id)
        
        return {
            "success": True,
            "model_id": model_id,
            "capabilities": capabilities
        }
    except Exception as e:
        logger.error(f"Error getting model capabilities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/models/registry",
    summary="List all models in registry",
    description="Get list of all models (loaded and unloaded)"
)
async def list_registry_models():
    """
    Get list of all models in the registry with capabilities.
    
    Returns:
        List of all registered models with their status and capabilities
    """
    try:
        models = model_registry.list_all_models()
        
        # Update loaded status and capabilities from model manager and detector
        for model in models:
            model['is_loaded'] = model_manager.is_model_loaded(model['model_id'])
            # Add capabilities info
            capabilities = model_detector.get_model_capabilities(model['model_id'])
            model['model_type'] = capabilities['model_type']
            model['supports_diarization'] = capabilities['supports_diarization']
            model['supports_timestamps'] = capabilities['supports_timestamps']
        
        return {
            "success": True,
            "models": models,
            "total_count": len(models),
            "loaded_count": sum(1 for m in models if m['is_loaded'])
        }
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/models/loaded",
    response_model=list[ModelInfo],
    summary="List loaded models",
    description="Get list of currently loaded models in memory"
)
async def list_loaded_models():
    """
    Get list of currently loaded models.
    
    Returns:
        List of ModelInfo objects for loaded models
    """
    loaded_models = model_manager.get_loaded_models()
    
    return [
        ModelInfo(
            model_id=model_id,
            is_loaded=True,
            model_type="audio"
        )
        for model_id in loaded_models
    ]


@router.get(
    "/models/recommended",
    summary="Get recommended models",
    description="Get list of recommended models for transcription"
)
async def get_recommended_models():
    """
    Get list of recommended models.
    
    Returns:
        List of recommended model IDs
    """
    return {
        "success": True,
        "recommended_models": model_registry.get_recommended_models()
    }


@router.post(
    "/models/load",
    summary="Load a model",
    description="Load a specific model into memory"
)
async def load_model_endpoint(model_id: str = Form(..., description="HuggingFace model ID")):
    """
    Load a specific model into memory.
    
    Args:
        model_id: HuggingFace model identifier
        
    Returns:
        Success status
    """
    try:
        logger.info(f"Loading model: {model_id}")
        
        # Add to registry if not present
        model_type = "whisper" if "whisper" in model_id.lower() else "other"
        model_registry.add_model(model_id, model_type)
        
        # Load the model
        success = await model_manager.load_model(model_id)
        
        if success:
            return {
                "success": True,
                "message": f"Model {model_id} loaded successfully",
                "model_id": model_id
            }
        else:
            raise HTTPException(status_code=500, detail=f"Failed to load model {model_id}")
            
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/models/unload",
    summary="Unload a model",
    description="Unload a model from memory"
)
async def unload_model_endpoint(model_id: str = Form(..., description="HuggingFace model ID")):
    """
    Unload a model from memory (but keep in registry).
    
    Args:
        model_id: HuggingFace model identifier
        
    Returns:
        Success status
    """
    try:
        logger.info(f"Unloading model: {model_id}")
        success = model_manager.unload_model(model_id)
        
        if success:
            return {
                "success": True,
                "message": f"Model {model_id} unloaded from memory",
                "model_id": model_id
            }
        else:
            return {
                "success": False,
                "message": f"Model {model_id} was not loaded",
                "model_id": model_id
            }
            
    except Exception as e:
        logger.error(f"Error unloading model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/models/delete",
    summary="Delete a model",
    description="Remove a model from registry and unload from memory"
)
async def delete_model_endpoint(model_id: str = Form(..., description="HuggingFace model ID")):
    """
    Delete a model completely (unload from memory and remove from registry).
    
    Args:
        model_id: HuggingFace model identifier
        
    Returns:
        Success status
    """
    try:
        logger.info(f"Deleting model: {model_id}")
        
        # Unload from memory if loaded
        if model_manager.is_model_loaded(model_id):
            model_manager.unload_model(model_id)
        
        # Remove from registry
        success = model_registry.remove_model(model_id)
        
        if success:
            return {
                "success": True,
                "message": f"Model {model_id} deleted successfully",
                "model_id": model_id
            }
        else:
            return {
                "success": False,
                "message": f"Model {model_id} not found in registry",
                "model_id": model_id
            }
            
    except Exception as e:
        logger.error(f"Error deleting model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Diarization Management Endpoints

@router.post(
    "/diarization/load",
    summary="Load diarization pipeline",
    description="Load pyannote/speaker-diarization-3.1 pipeline"
)
async def load_diarization_pipeline(
    hf_token: Optional[str] = Form(
        default=None,
        description="HuggingFace token (required for pyannote models)"
    )
):
    """
    Load the pyannote diarization pipeline.
    
    Note: pyannote models require accepting the license at:
    https://huggingface.co/pyannote/speaker-diarization-3.1
    
    Args:
        hf_token: Optional HuggingFace authentication token
        
    Returns:
        Success status
    """
    try:
        logger.info("Loading diarization pipeline...")
        success = await diarization_service.load_pipeline(hf_token)
        
        if success:
            return {
                "success": True,
                "message": "Diarization pipeline loaded successfully",
                "model": diarization_service.DIARIZATION_MODEL
            }
        else:
            return {
                "success": False,
                "message": (
                    "Failed to load diarization pipeline. "
                    "Make sure you have accepted the license at "
                    "https://huggingface.co/pyannote/speaker-diarization-3.1 "
                    "and provided a valid HuggingFace token."
                ),
                "model": diarization_service.DIARIZATION_MODEL
            }
            
    except Exception as e:
        logger.error(f"Error loading diarization pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/diarization/unload",
    summary="Unload diarization pipeline",
    description="Unload diarization pipeline from memory"
)
async def unload_diarization_pipeline():
    """
    Unload the pyannote diarization pipeline from memory.
    
    Returns:
        Success status
    """
    try:
        logger.info("Unloading diarization pipeline...")
        await diarization_service.unload_pipeline()
        
        return {
            "success": True,
            "message": "Diarization pipeline unloaded successfully"
        }
        
    except Exception as e:
        logger.error(f"Error unloading diarization pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/diarization/status",
    summary="Get diarization status",
    description="Check if diarization pipeline is loaded"
)
async def get_diarization_status():
    """
    Get the status of the diarization pipeline.
    
    Returns:
        Status information
    """
    try:
        is_loaded = diarization_service.is_loaded()
        
        return {
            "success": True,
            "is_loaded": is_loaded,
            "model": diarization_service.DIARIZATION_MODEL,
            "message": "Diarization available" if is_loaded else "Diarization not loaded"
        }
        
    except Exception as e:
        logger.error(f"Error checking diarization status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
