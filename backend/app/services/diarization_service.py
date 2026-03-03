"""Speaker diarization service using pyannote.audio."""

from typing import List, Dict, Optional
import numpy as np
import torch
from pathlib import Path
from pyannote.audio import Pipeline
from app.core.logging import get_logger
from app.core.config import get_settings

logger = get_logger(__name__)
settings = get_settings()


class DiarizationService:
    """Service for speaker diarization using pyannote.audio."""
    
    # Pyannote model for speaker diarization
    DIARIZATION_MODEL = "pyannote/speaker-diarization-3.1"
    
    def __init__(self):
        """Initialize diarization service."""
        self.pipeline: Optional[Pipeline] = None
        self.sample_rate = 16000
    
    def is_loaded(self) -> bool:
        """Check if diarization pipeline is loaded."""
        return self.pipeline is not None
    
    async def load_pipeline(self, hf_token: Optional[str] = None) -> bool:
        """
        Load pyannote diarization pipeline.
        
        Args:
            hf_token: HuggingFace token (optional, uses config if not provided)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.is_loaded():
                logger.info("Diarization pipeline already loaded")
                return True
            
            logger.info(f"Loading diarization pipeline: {self.DIARIZATION_MODEL}")
            
            # Get token from parameter or config
            token = hf_token or settings.HUGGINGFACE_TOKEN
            
            if not token:
                logger.error(
                    "HuggingFace token not provided. "
                    "Set HUGGINGFACE_TOKEN in .env file or pass hf_token parameter."
                )
                raise Exception(
                    "HuggingFace token required for pyannote models. "
                    "Please set HUGGINGFACE_TOKEN in your .env file"
                )
            
            # Load the pipeline with authentication
            logger.info("Loading pipeline with HuggingFace authentication...")
            self.pipeline = Pipeline.from_pretrained(
                self.DIARIZATION_MODEL,
                use_auth_token=token
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                self.pipeline.to(torch.device("cuda"))
                logger.info("Diarization pipeline moved to GPU")
            
            logger.info("Diarization pipeline loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading diarization pipeline: {str(e)}")
            logger.warning(
                f"Failed to load {self.DIARIZATION_MODEL}. "
                "Make sure you have accepted the model license at "
                "https://huggingface.co/pyannote/speaker-diarization-3.1 "
                "and set your HuggingFace token in the environment."
            )
            self.pipeline = None
            return False
    
    async def unload_pipeline(self):
        """Unload diarization pipeline from memory."""
        try:
            if self.pipeline is not None:
                del self.pipeline
                self.pipeline = None
                
                # Clear GPU cache if using CUDA
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                logger.info("Diarization pipeline unloaded")
                
        except Exception as e:
            logger.error(f"Error unloading diarization pipeline: {str(e)}")
    
    async def diarize(
        self,
        audio_path: str,
        num_speakers: Optional[int] = None,
        min_speakers: Optional[int] = None,
        max_speakers: Optional[int] = None
    ) -> List[Dict]:
        """
        Perform speaker diarization on audio file.
        
        Args:
            audio_path: Path to audio file
            num_speakers: Expected number of speakers (optional)
            min_speakers: Minimum number of speakers (optional)
            max_speakers: Maximum number of speakers (optional)
            
        Returns:
            List of diarization segments with format:
            [
                {
                    "channel": int (speaker ID),
                    "offset": float (start time in seconds),
                    "duration": float (duration in seconds),
                    "speaker": str (speaker label like SPEAKER_00)
                }
            ]
        """
        try:
            if not self.is_loaded():
                logger.error("Diarization pipeline not loaded")
                raise Exception(
                    "Diarization pipeline not loaded. "
                    "Please ensure pyannote model is properly configured."
                )
            
            logger.info(f"Performing diarization on: {audio_path}")
            
            # Prepare pipeline parameters
            pipeline_params = {}
            if num_speakers is not None:
                pipeline_params["num_speakers"] = num_speakers
            if min_speakers is not None:
                pipeline_params["min_speakers"] = min_speakers
            if max_speakers is not None:
                pipeline_params["max_speakers"] = max_speakers
            
            # Run diarization
            diarization = self.pipeline(audio_path, **pipeline_params)
            
            # Convert to our segment format
            segments = []
            speaker_map = {}  # Map speaker labels to channel IDs
            next_channel = 0
            
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                # Map speaker label to channel ID
                if speaker not in speaker_map:
                    speaker_map[speaker] = next_channel
                    next_channel += 1
                
                channel = speaker_map[speaker]
                
                segments.append({
                    "channel": channel,
                    "offset": round(turn.start, 2),
                    "duration": round(turn.duration, 2),
                    "speaker": speaker
                })
            
            logger.info(
                f"Diarization completed: {len(segments)} segments, "
                f"{len(speaker_map)} speakers detected"
            )
            
            return segments
            
        except Exception as e:
            logger.error(f"Error during diarization: {str(e)}")
            raise
    
    async def align_with_transcription(
        self,
        diarization_segments: List[Dict],
        transcription: str,
        audio_duration: float
    ) -> List[Dict]:
        """
        Align diarization segments with transcription text.
        
        This creates speaker-labeled text segments by distributing
        the transcription text across diarization time segments.
        
        Args:
            diarization_segments: Speaker diarization segments
            transcription: Full transcription text
            audio_duration: Total audio duration in seconds
            
        Returns:
            List of aligned segments with text
        """
        try:
            if not diarization_segments:
                logger.warning("No diarization segments to align")
                return []
            
            # Split transcription into words
            words = transcription.split()
            if not words:
                return diarization_segments
            
            total_words = len(words)
            words_per_second = total_words / audio_duration if audio_duration > 0 else 0
            
            aligned_segments = []
            word_index = 0
            
            for segment in diarization_segments:
                offset = segment["offset"]
                duration = segment["duration"]
                
                # Calculate how many words should be in this segment
                expected_words = int(duration * words_per_second)
                expected_words = max(1, expected_words)  # At least 1 word
                
                # Get words for this segment
                segment_words = words[word_index:word_index + expected_words]
                word_index += len(segment_words)
                
                # Create aligned segment
                aligned_segments.append({
                    "channel": segment["channel"],
                    "offset": segment["offset"],
                    "duration": segment["duration"],
                    "text": " ".join(segment_words),
                    "speaker": segment.get("speaker", f"SPEAKER_{segment['channel']:02d}")
                })
                
                # Stop if we've used all words
                if word_index >= total_words:
                    break
            
            # If there are remaining words, add them to the last segment
            if word_index < total_words and aligned_segments:
                remaining_words = words[word_index:]
                aligned_segments[-1]["text"] += " " + " ".join(remaining_words)
            
            logger.info(f"Aligned {len(aligned_segments)} segments with transcription")
            return aligned_segments
            
        except Exception as e:
            logger.error(f"Error aligning transcription: {str(e)}")
            # Return segments without text on error
            return diarization_segments
    
    def create_fallback_segments(
        self,
        transcription: str,
        audio_duration: float,
        num_speakers: int = 2
    ) -> List[Dict]:
        """
        Create fallback diarization segments when pyannote is not available.
        
        This is a simple time-based segmentation for graceful degradation.
        
        Args:
            transcription: Full transcription text
            audio_duration: Audio duration in seconds
            num_speakers: Number of speakers to simulate
            
        Returns:
            List of simple segments
        """
        logger.warning("Using fallback segmentation (pyannote not available)")
        
        segments = []
        sentences = [s.strip() + "." for s in transcription.split('.') if s.strip()]
        
        if not sentences:
            return []
        
        avg_duration = audio_duration / len(sentences)
        current_offset = 0.0
        
        for i, sentence in enumerate(sentences):
            # Estimate duration based on text length
            words = sentence.split()
            duration = max(avg_duration, len(words) * 0.4)
            
            # Distribute speakers evenly
            channel = i % num_speakers
            
            segments.append({
                "channel": channel,
                "offset": round(current_offset, 2),
                "duration": round(min(duration, audio_duration - current_offset), 2),
                "text": sentence,
                "speaker": f"SPEAKER_{channel:02d}"
            })
            
            current_offset += duration
            
            if current_offset >= audio_duration:
                break
        
        return segments


# Global diarization service instance
diarization_service = DiarizationService()
