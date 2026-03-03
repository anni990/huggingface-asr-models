"""Audio transcription service."""

import torch
import librosa
import soundfile as sf
import warnings
from pathlib import Path
from typing import Optional, Tuple, List, Dict
import numpy as np
from app.core.logging import get_logger
from app.services.model_loader import model_manager
from app.services.model_detector import model_detector
from app.services.diarization_service import diarization_service

logger = get_logger(__name__)

# Suppress MP3 decoder warnings (non-fatal encoding issues)
warnings.filterwarnings('ignore', message='.*MPEG_LAYER_III subtype is unknown.*')
warnings.filterwarnings('ignore', message='.*part2_3_length.*too large.*')


class TranscriptionService:
    """Service for audio transcription using HuggingFace models."""
    
    def __init__(self):
        """Initialize transcription service."""
        self.sample_rate = 16000  # Standard for most ASR models
    
    async def load_audio(self, audio_path: str) -> Tuple[np.ndarray, float]:
        """
        Load and preprocess audio file.
        
        Note: Some MP3 files may produce non-fatal decoder warnings.
        These are automatically suppressed and do not affect transcription quality.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Tuple of (audio_array, duration)
        """
        try:
            import sys
            import os
            
            # Suppress C-level stderr warnings from MP3 decoder
            # (e.g., "part2_3_length too large" - non-fatal encoding issues)
            stderr_fileno = sys.stderr.fileno()
            old_stderr = os.dup(stderr_fileno)
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, stderr_fileno)
            
            try:
                # Load audio with librosa
                audio_array, sr = librosa.load(audio_path, sr=self.sample_rate)
                duration = librosa.get_duration(y=audio_array, sr=sr)
            finally:
                # Restore stderr
                os.dup2(old_stderr, stderr_fileno)
                os.close(old_stderr)
                os.close(devnull)
            
            logger.info(f"Loaded audio: duration={duration:.2f}s, sample_rate={sr}")
            return audio_array, duration
            
        except Exception as e:
            logger.error(f"Error loading audio: {str(e)}")
            raise
    
    async def transcribe(
        self,
        audio_path: str,
        model_id: str,
        enable_diarization: bool = False
    ) -> Tuple[str, Optional[List[Dict]], float]:
        """
        Transcribe audio file using specified model (GENERIC - works with any HuggingFace ASR model).
        
        Args:
            audio_path: Path to audio file
            model_id: HuggingFace model identifier (any ASR model)
            enable_diarization: Whether to perform speaker diarization using pyannote
            
        Returns:
            Tuple of (transcribed_text, diarization_segments, audio_duration)
        """
        try:
            # Ensure model is loaded
            if not model_manager.is_model_loaded(model_id):
                logger.info(f"Model {model_id} not loaded, loading now...")
                success = await model_manager.load_model(model_id)
                if not success:
                    raise Exception(f"Failed to load model: {model_id}")
            
            # Get model and processor
            model = model_manager.get_model(model_id)
            processor = model_manager.get_processor(model_id)
            
            # Load audio
            audio_array, duration = await self.load_audio(audio_path)
            
            # Detect model type
            model_type = model_detector.detect_model_type(model_id)
            logger.info(f"Using model type: {model_type}")
            
            # Route to appropriate transcription method based on model type
            if model_type == "qwen":
                transcription = await self._transcribe_qwen(
                    audio_array, model, processor
                )
            elif model_type == "whisper":
                transcription = await self._transcribe_whisper(
                    audio_array, model, processor
                )
            else:
                # Generic ASR model (wav2vec2, hubert, seamless, etc.)
                transcription = await self._transcribe_generic(
                    audio_array, model, processor
                )
            
            logger.info(f"Transcription completed: {len(transcription)} characters")
            
            # Perform diarization if requested using pyannote
            diarization_segments = None
            if enable_diarization:
                diarization_segments = await self._perform_diarization(
                    audio_path, transcription, duration
                )
            
            return transcription, diarization_segments, duration
            
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise
    
    async def _transcribe_qwen(
        self,
        audio_array: np.ndarray,
        model,
        processor
    ) -> str:
        """Transcribe using Qwen2-Audio models."""
        try:
            # Prepare conversation for Qwen2-Audio
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {"type": "audio", "audio": audio_array},
                        {"type": "text", "text": "Transcribe the speech to text."}
                    ]
                }
            ]
            
            # Apply chat template and prepare inputs
            text = processor.apply_chat_template(
                conversation,
                add_generation_prompt=True,
                tokenize=False
            )
            
            # Process audio and text
            inputs = processor(
                text=[text],
                audios=[audio_array],
                sampling_rate=self.sample_rate,
                return_tensors="pt",
                padding=True
            )
            
            # Move inputs to device
            inputs = inputs.to(model.device)
            
            # Generate transcription
            with torch.no_grad():
                generated_ids = model.generate(
                    **inputs,
                    max_new_tokens=512
                )
            
            # Trim and decode
            generated_ids = generated_ids[:, inputs.input_ids.size(1):]
            transcription = processor.batch_decode(
                generated_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )[0]
            
            return transcription.strip()
            
        except Exception as e:
            logger.error(f"Error in Qwen transcription: {str(e)}")
            raise
    
    async def _transcribe_whisper(
        self,
        audio_array: np.ndarray,
        model,
        processor
    ) -> str:
        """Transcribe using Whisper models."""
        try:
            # Process inputs
            inputs = processor(
                audio_array,
                sampling_rate=self.sample_rate,
                return_tensors="pt"
            )
            
            # Move to device
            inputs = inputs.to(model.device)
            
            # Generate transcription
            with torch.no_grad():
                generated_ids = model.generate(**inputs)
            
            # Decode
            transcription = processor.batch_decode(
                generated_ids,
                skip_special_tokens=True
            )[0]
            
            return transcription.strip()
            
        except Exception as e:
            logger.error(f"Error in Whisper transcription: {str(e)}")
            raise
    
    async def _transcribe_generic(
        self,
        audio_array: np.ndarray,
        model,
        processor
    ) -> str:
        """Transcribe using generic HuggingFace ASR models (Wav2Vec2, Hubert, etc.)."""
        try:
            # Process inputs
            inputs = processor(
                audio_array,
                sampling_rate=self.sample_rate,
                return_tensors="pt"
            )
            
            # Move to device
            inputs = inputs.to(model.device)
            
            # Generate transcription
            with torch.no_grad():
                generated_ids = model.generate(**inputs)
            
            # Decode
            transcription = processor.batch_decode(
                generated_ids,
                skip_special_tokens=True
            )[0]
            
            return transcription.strip()
            
        except Exception as e:
            logger.error(f"Error in generic transcription: {str(e)}")
            raise
    
    async def _perform_diarization(
        self,
        audio_path: str,
        transcription: str,
        audio_duration: float
    ) -> List[Dict]:
        """
        Perform speaker diarization using pyannote.audio.
        
        This method uses the dedicated pyannote/speaker-diarization-3.1 model
        which works universally with any transcription model.
        
        Args:
            audio_path: Path to audio file
            transcription: Full transcription text
            audio_duration: Audio duration in seconds
            
        Returns:
            List of diarization segments with speaker-labeled text
        """
        try:
            # Ensure diarization pipeline is loaded
            if not diarization_service.is_loaded():
                logger.info("Loading pyannote diarization pipeline...")
                success = await diarization_service.load_pipeline()
                if not success:
                    logger.warning("Failed to load diarization pipeline, using fallback")
                    return diarization_service.create_fallback_segments(
                        transcription, audio_duration
                    )
            
            # Perform diarization
            logger.info("Performing speaker diarization with pyannote...")
            diarization_segments = await diarization_service.diarize(audio_path)
            
            # Align diarization with transcription text
            aligned_segments = await diarization_service.align_with_transcription(
                diarization_segments, transcription, audio_duration
            )
            
            logger.info(f"Diarization complete: {len(aligned_segments)} speaker segments")
            return aligned_segments
            
        except Exception as e:
            logger.error(f"Error in diarization: {str(e)}")
            logger.warning("Falling back to simple segmentation")
            # Fallback to simple segmentation
            return diarization_service.create_fallback_segments(
                transcription, audio_duration
            )


# Global transcription service instance
transcription_service = TranscriptionService()
