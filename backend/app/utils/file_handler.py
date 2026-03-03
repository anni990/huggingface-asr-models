"""File handling utilities."""

import os
import aiofiles
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class FileHandler:
    """Handles file operations for uploaded audio."""
    
    def __init__(self):
        """Initialize file handler."""
        self.upload_dir = Path("temp/uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_upload_file(self, upload_file: UploadFile) -> str:
        """
        Save uploaded file to temporary directory.
        
        Args:
            upload_file: FastAPI UploadFile object
            
        Returns:
            Path to saved file
        """
        try:
            # Validate file extension
            file_ext = Path(upload_file.filename).suffix.lower()
            if file_ext not in settings.allowed_formats_list:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file format. Allowed: {settings.ALLOWED_AUDIO_FORMATS}"
                )
            
            # Generate safe filename
            safe_filename = f"{os.urandom(16).hex()}{file_ext}"
            file_path = self.upload_dir / safe_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = await upload_file.read()
                
                # Check file size
                if len(content) > settings.max_audio_size_bytes:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File too large. Max size: {settings.MAX_AUDIO_SIZE_MB}MB"
                    )
                
                await f.write(content)
            
            logger.info(f"Saved upload file: {file_path}")
            return str(file_path)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    async def delete_file(self, file_path: str) -> bool:
        """
        Delete a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if deleted successfully
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    async def cleanup_old_files(self, max_age_seconds: int = 3600) -> int:
        """
        Clean up old temporary files.
        
        Args:
            max_age_seconds: Maximum age of files to keep
            
        Returns:
            Number of files deleted
        """
        import time
        deleted = 0
        
        try:
            for file_path in self.upload_dir.iterdir():
                if file_path.is_file():
                    file_age = time.time() - file_path.stat().st_mtime
                    if file_age > max_age_seconds:
                        file_path.unlink()
                        deleted += 1
            
            if deleted > 0:
                logger.info(f"Cleaned up {deleted} old files")
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return deleted


# Global file handler instance
file_handler = FileHandler()
